import pandas

from django.db.models import Count

from profiles.models import Membership, Profile, School, Address


class UpdateSchoolsCVTI:

    def __init__(self, file, store_changes_in_db=False):
        self.file = file
        self.df = pandas.read_csv(file, sep=';', dtype=str)
        self.test_run = not store_changes_in_db

    def execute(self):
        return self.add_leading_zero()

    def delete_child_schools(self):
        """
        Delete Child schools if it has no members. Child schools with members are skipped.
        GPS coordinates are transferred to parent schools (which are created if they do not exist).
        """

        school_change_messages = []

        # Select schools that are not part of a bigger school (based in their EDUID)
        df_merged = self.df.drop(self.df[self.df.EDUID == self.df.KmenovaSaSZ_EDUID].index)

        schools = School.objects.all()
        kodsko_cvti_merged = df_merged["KODSKO"].values.tolist()

        i = 0
        for school in schools:

            # If a schools has a 'parent' deal with it
            if school.school_code and school.school_code in kodsko_cvti_merged:

                new_school_code_series = df_merged.loc[df_merged['KODSKO'] == school.school_code, 'KmenovaSaSZ_KODSKO']

                old_school_code = school.school_code

                if new_school_code_series.size:
                    school.school_code = new_school_code_series.iloc[0]

                    if self.test_run:
                        msg_prefix = f"DRY RUN: "
                    else:
                        msg_prefix = ""
                        school.save()

                    school_change_messages.append(f"{msg_prefix}CHANGE OF CODE from {old_school_code} "
                                                  f"to {school.school_code}, "
                                                  f"{school}, {school.members.all().count()} members")

        return school_change_messages

    def delete_duplicate_school_codes(self):
        msg = []

        dup_schools = School.objects.values('school_code').annotate(school_code_count=Count('school_code'))
        dup_schools = dup_schools.exclude(school_code_count=1).order_by('school_code')

        for school_code in dup_schools:
            schools = School.objects.filter(school_code=school_code['school_code'])

            all_members = 0
            for school in schools:
                members = school.members.all().count()
                all_members += members

            if all_members == 0:

                school = schools[0]
                members = school.members.all().count()
                msg.append(f"LEAVING {school.school_code}, {school}, {members} members")

                for school in schools[1:]:
                    members = school.members.all().count()
                    if self.test_run:
                        msg.append(f"WOULD DELETE {school.school_code}, {school}, {members} members")
                    else:
                        msg.append(f"DELETING {school.school_code}, {school}, {members} members")
                        school.delete()
            else:
                for school in schools:
                    members = school.members.all().count()
                    msg.append(f"LEAVING {school.school_code}, {school}, {members} members")

        return msg

    def overview(self):

        changes_in_db_paired = []
        changes_in_db_unpaired_new = []
        changes_in_db_unpaired_old = []
        changes_in_db_error = []

        # Drop schools that are part of a bigger school (based in their EDUID)
        df = self.df.drop(self.df[self.df.EDUID != self.df.KmenovaSaSZ_EDUID].index)

        # Drop canteens and other types of school institutions (except schools)
        df = df.drop(df[df.Hierarchia == "Školské zariadenie"].index)

        # Drop Cancelled Schools
        df = df.drop(df[df.DatumZaniku.notnull()].index)

        # Drop nurseries, language schools and art schools
        df = df.drop(df[df.DruhSaSZ.isin(["jazyková škola", "materská škola", "základná umelecká škola"])].index)

        typ_sasz_to_del = [
            "MŠ pri zdravotníckom zariadení",
            "ŠMŠ pre deti s autizmom",
            "ŠMŠ pre deti s narušenou komunikačnou schopnosťou",
            "ŠMŠ pre deti s narušenou komunikačnou schopnosťou internátna",
            "ŠMŠ pre deti so sluchovým postihnutím internátna",
            "ŠMŠ pre deti so zrakovým postihnutím",
            "ŠMŠ pre deti so zrakovým postihnutím internátna",
            "ŠMŠ pre deti s telesným postihnutím",
            "ŠMŠ pre deti s viacnásobným postihnutím internátna",
            "ŠMŠ pri špeciálnom výchovnom zariadení",
            "Špeciálna materská škola",
            "Špec.materská škola internátna",
        ]
        df = df.drop(df[df.TypSaSZ.isin(typ_sasz_to_del)].index)

        for index, row in df.iterrows():
            school = School.objects.filter(school_code=row['KODSKO'])
            change = f"{row['EDUID']}, {row['KODSKO']}, {row['ICO']}, {row['Nazov']}, {school}"

            if school.count() == 1:
                changes_in_db_paired.append(change)
            elif school.count() > 1:
                changes_in_db_error.append(change)
            else:
                if self.test_run:
                    msg_prefix = f"WOULD ADD: "
                else:
                    msg_prefix = "ADDING: "

                    if row['Ulica'] is not pandas.np.nan:
                        street = f"{row['Ulica']}"
                    else:
                        street = f"{row['Obec']}"

                    if row['SupisneCislo'] is not pandas.np.nan and row['OrientacneCislo'] is not pandas.np.nan:
                        street += f" {row['SupisneCislo']}/{row['OrientacneCislo']}"
                    elif row['SupisneCislo'] is not pandas.np.nan:
                        street += f" {row['SupisneCislo']}"
                    else:
                        street += f" {row['OrientacneCislo']}"

                    new_address = Address(
                        street=street,
                        city=f"{row['Obec']}",
                        postal_code=f"{row['PSC']}",
                        country='SK',
                    )
                    new_address.save()

                    new_school = School(
                        name=row['Nazov'],
                        description="",
                        address=new_address,
                        district=row['Okres'],
                        region=row['Kraj'],
                        founder=row['Zriadovatel_Typ'],
                        school_type=row['TypSaSZ'],
                        school_code=row['KODSKO'],
                        edu_id=row['EDUID'],
                        mail=row['Email'],
                        website=row['Web'],
                    )
                    new_school.save()
                changes_in_db_unpaired_new.append(msg_prefix + change)

        schools = School.objects.all()
        kodsko_cvti = df["KODSKO"].values.tolist()

        for school in schools:
            change = f"{school.school_code}, {school.edu_id}, {school}, {school.members.all().count()} memberships"
            if school.school_code and school.school_code not in kodsko_cvti:
                if school.members.all().count() == 0:
                    if self.test_run:
                        msg_prefix = f"WOULD DELETE: "
                    else:
                        msg_prefix = "DELETING: "
                        school.delete()
                else:
                    msg_prefix = "LEAVING: "
                changes_in_db_unpaired_old.append(msg_prefix + change)

        school_change_messages = [
            f"**changes_in_db_paired {len(changes_in_db_paired)}**",
            *changes_in_db_paired,
            f"**changes_in_db_unpaired_new {len(changes_in_db_unpaired_new)}**",
            *changes_in_db_unpaired_new,
            f"**changes_in_db_unpaired_old {len(changes_in_db_unpaired_old)}**",
            *changes_in_db_unpaired_old,
            f"**changes_in_db_error {len(changes_in_db_error)}**",
            *changes_in_db_error,
        ]

        return school_change_messages

    def add_leading_zero(self):
        schools = School.objects.all()

        school_change_messages = []

        for school in schools:
            if school.school_code and len(school.school_code) != 9:
                school.school_code = str(school.school_code).zfill(9)
                school.save()
                school_change_messages.append(f"CHANGING: {school.school_code}")

        return school_change_messages

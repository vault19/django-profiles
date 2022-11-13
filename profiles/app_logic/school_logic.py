import pandas

from django.db.models import Count

from profiles.models import Membership, Profile, School


class UpdateSchoolsCVTI:

    def __init__(self, file, store_changes_in_db=False):
        self.file = file
        self.df = pandas.read_csv(file, sep=';')
        self.test_run = not store_changes_in_db

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
            if school.school_code and int(school.school_code) in kodsko_cvti_merged:

                new_school_code_series = df_merged.loc[df_merged['KODSKO'] == int(school.school_code), 'KmenovaSaSZ_KODSKO']

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

        # Drop nurseries, language schools and art schools
        df = df.drop(df[df.DruhSaSZ.isin(["jazyková škola", "materská škola", "základná umelecká škola"])].index)

        for index, row in df.iterrows():
            school = School.objects.filter(school_code=row['KODSKO'])
            change = f"{row['EDUID']}, {row['KODSKO']}, {row['ICO']}, {row['Nazov']}, {school}"

            if school.count() == 1:
                changes_in_db_paired.append(change)
            elif school.count() > 1:
                changes_in_db_error.append(change)
            else:
                changes_in_db_unpaired_new.append(change)

        schools = School.objects.all()
        kodsko_cvti = df["KODSKO"].values.tolist()

        for school in schools:
            change = f"{school.school_code}, {school.edu_id}, {school}, {school.members.all().count()} memberships"
            if school.school_code and int(school.school_code) not in kodsko_cvti:
                changes_in_db_unpaired_old.append(change)

        school_change_messages = [
            f"**changes_in_db_paired {len(changes_in_db_paired)}**",
            changes_in_db_paired,
            f"**changes_in_db_unpaired_new {len(changes_in_db_unpaired_new)}**",
            changes_in_db_unpaired_new,
            f"**changes_in_db_unpaired_old {len(changes_in_db_unpaired_old)}**",
            changes_in_db_unpaired_old,
            f"**changes_in_db_error {len(changes_in_db_error)}**",
            changes_in_db_error,
        ]

        return school_change_messages

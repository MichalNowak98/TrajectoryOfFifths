import csv


class CsvManager:
    __csv_content = [
        ['', '32 fragments', '', '', '16 fragments', '', '', '8 fragments', '', ''],
        ['', 'whole-note', 'trajectory signature', 'dur/moll points ratio', 'whole-note', 'trajectory signature', 'dur/moll points ratio', 'whole-note', 'trajectory signature', 'dur/moll points ratio'],
        ['', '', '', '', '', '', '', '', '', ''],
        ['', 'half-note', 'trajectory signature', 'dur/moll points ratio', 'half-note', 'trajectory signature', 'dur/moll points ratio', 'half-note', 'trajectory signature', 'dur/moll points ratio'],
        ['', '', '', '', '', '', '', '', '', ''],
        ['', 'quarter-note', 'trajectory signature', 'dur/moll points ratio', 'quarter-note', 'trajectory signature', 'dur/moll points ratio', 'quarter-note', 'trajectory signature', 'dur/moll points ratio'],
        ['', '', '', '', '', '', '', '', '', ''],
        ['', 'quaver-note', 'trajectory signature', 'dur/moll points ratio', 'quaver-note', 'trajectory signature', 'dur/moll points ratio', 'quaver-note', 'trajectory signature', 'dur/moll points ratio'],
        ['', '', '', '', '', '', '', '', '', ''],
        ['', 'semiquaver-note', 'trajectory signature', 'dur/moll points ratio', 'semiquaver-note', 'trajectory signature', 'dur/moll points ratio', 'semiquaver-note', 'trajectory signature', 'dur/moll points ratio'],
        ['', '', '', '', '', '', '', '', '', ''],
    ]

    def save_data_to_csv(self, track_name):
        with open('trajectory_data_5.csv', mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file, dialect='excel', delimiter=';')
            self.__csv_content[0][0] = track_name
            writer.writerows(self.__csv_content)

    def fill_data_32_whole(self, signature, quarter_point_counts):
        self.__csv_content[2][2] = signature
        self.__csv_content[2][3] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_32_half(self, signature, quarter_point_counts):
        self.__csv_content[4][2] = signature
        self.__csv_content[4][3] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_32_quarter(self, signature, quarter_point_counts):
        self.__csv_content[6][2] = signature
        self.__csv_content[6][3] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_32_quaver(self, signature, quarter_point_counts):
        self.__csv_content[8][2] = signature
        self.__csv_content[8][3] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_32_semiquaver(self, signature, quarter_point_counts):
        self.__csv_content[10][2] = signature
        self.__csv_content[10][3] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_16_whole(self, signature, quarter_point_counts):
        self.__csv_content[2][5] = signature
        self.__csv_content[2][6] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_16_half(self, signature, quarter_point_counts):
        self.__csv_content[4][5] = signature
        self.__csv_content[4][6] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_16_quarter(self, signature, quarter_point_counts):
        self.__csv_content[6][5] = signature
        self.__csv_content[6][6] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_16_quaver(self, signature, quarter_point_counts):
        self.__csv_content[8][5] = signature
        self.__csv_content[8][6] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_16_semiquaver(self, signature, quarter_point_counts):
        self.__csv_content[10][5] = signature
        self.__csv_content[10][6] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_8_whole(self, signature, quarter_point_counts):
        self.__csv_content[2][8] = signature
        self.__csv_content[2][9] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_8_half(self, signature, quarter_point_counts):
        self.__csv_content[4][8] = signature
        self.__csv_content[4][9] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_8_quarter(self, signature, quarter_point_counts):
        self.__csv_content[6][8] = signature
        self.__csv_content[6][9] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_8_quaver(self, signature, quarter_point_counts):
        self.__csv_content[8][8] = signature
        self.__csv_content[8][9] = f"{self.calculate_ratio(quarter_point_counts)}"

    def fill_data_8_semiquaver(self, signature, quarter_point_counts):
        self.__csv_content[10][8] = signature
        self.__csv_content[10][9] = f"{self.calculate_ratio(quarter_point_counts)}"
        
    @staticmethod
    def calculate_ratio(quarter_point_counts):
        # if quarter_point_counts[1] == 0:
        #     return "dur"
        # x = quarter_point_counts[0]/quarter_point_counts[1]
        # value = str(quarter_point_counts[0]/quarter_point_counts[1])
        # return value.replace(".", ",")
        return f"{quarter_point_counts[0]} to {quarter_point_counts[1]}"


from sys import argv
import time


class Spot:

    digit = None
    domain = None
    neighbours = None

    def __init__(self, num, domain):
        self.digit = num
        self.domain = domain
        self.neighbours = []

    def __str__(self):
        return self.digit


class SudokuGrid:

    def __init__(self, digits_string):
        self.__grid = []
        self.__empty_spots = []  # MRB

        row_num = 0
        col_num = 0
        row = []
        for digit in digits_string:
            if digit == '.':
                spot = Spot(0, list(range(1, 10)))

                # Get neighbours coordinates.
                row_neighbours = list(map(lambda elem: tuple([row_num, elem]), range(9)))
                col_neighbours = list(map(lambda elem: tuple([elem, col_num]), range(9)))
                rs = row_num - row_num % 3  # Square Row start.
                cs = col_num - col_num % 3  # Square Col start.
                square_neighbours = [(rs, cs), (rs, cs + 1), (rs, cs + 2), (rs + 1, cs), (rs + 1, cs + 1),
                                     (rs + 1, cs + 2), (rs + 2, cs), (rs + 2, cs + 1), (rs + 2, cs + 2)]
                # Remove duplicates
                neighbour_positions = list(set(row_neighbours + col_neighbours + square_neighbours))
                neighbour_positions.remove(tuple([row_num, col_num]))

                # At the beginning, neighbours are spots positions.
                # Later, in __setup_domains method, they are changed to actual neighbour spot objects.
                spot.neighbours = neighbour_positions

                row.append(spot)
                self.__empty_spots.append(spot)
            else:
                row.append(Spot(int(digit), None))

            if col_num == 8:
                self.__grid.append(row)
                row_num += 1
                col_num = 0
                row = []
            else:
                col_num += 1

        self.__setup_domains()

    # Sets domains for each point with constraints.
    def __setup_domains(self):
        for spot in self.__empty_spots:
            neighbours = self.__get_neighbours(spot.neighbours)
            for neighbour in neighbours:
                if neighbour.digit != 0 and neighbour.digit in spot.domain:
                    spot.domain.remove(neighbour.digit)
            spot.neighbours = neighbours

    # Returns list of spots form corresponding positions.
    def __get_neighbours(self, positions):
        result = []
        for pos in positions:
            result.append(self.__grid[pos[0]][pos[1]])
        return result

    def print(self):
        for row_num in range(len(self.__grid)):
            row = ''
            for col_num in range(len(self.__grid[row_num])):
                row += str(self.__grid[row_num][col_num].digit) + ' '
            print(row.strip())

    def __str__(self):
        result = ''
        for i in range(9):
            for j in range(9):
                result += str(self.__grid[i][j].digit)
        return result

    def solve(self):
        if len(self.__empty_spots) == 0:
            return True

        spot = min(self.__empty_spots, key=lambda elem: len(elem.domain))  # MRB
        self.__empty_spots.remove(spot)

        for digit in spot.domain:
            spot.digit = digit

            changed_neighbours = []
            for neighbour in spot.neighbours:  # Remove digit from neighbour domains.
                if neighbour.digit == 0 and digit in neighbour.domain:
                    neighbour.domain.remove(digit)
                    changed_neighbours.append(neighbour)

            if self.solve():
                return True
            else:
                spot.digit = 0
                for neighbour in changed_neighbours:  # Add back digit to neighbour domains.
                    neighbour.domain.append(digit)
        self.__empty_spots.append(spot)
        return False


def main():
    input_filename = argv[1]
    output_filename = argv[2]

    input_file = open(input_filename)
    output_file = open(output_filename, 'w')
    start_time = time.time()
    while True:
        digits = input_file.readline().strip()
        if len(digits) != 81:
            break
        sudoku_grid = SudokuGrid(digits)
        sudoku_grid.solve()
        output_file.write(str(sudoku_grid) + '\n')
    input_file.close()
    output_file.close()
    print(time.time() - start_time, 'Seconds')


if __name__ == '__main__':
    main()

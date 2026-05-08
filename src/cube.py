class RubiksCube:
    """
    A simple Rubik's Cube representation.

    Each face is represented as a list of 9 stickers.

    Sticker indexes on each face:

        0 1 2
        3 4 5
        6 7 8

    Face order:
    U = Up
    D = Down
    F = Front
    B = Back
    R = Right
    L = Left
    """

    def __init__(self):
        """
        Create a solved Rubik's Cube.
        """
        self.faces = {
            "U": ["W"] * 9,
            "D": ["Y"] * 9,
            "F": ["G"] * 9,
            "B": ["B"] * 9,
            "R": ["R"] * 9,
            "L": ["O"] * 9,
        }

    def display(self):
        """
        Print the current cube state in a readable format.
        """
        for face_name, stickers in self.faces.items():
            print(f"{face_name} face:")
            print(stickers[0], stickers[1], stickers[2])
            print(stickers[3], stickers[4], stickers[5])
            print(stickers[6], stickers[7], stickers[8])
            print()

    def is_solved(self):
        """
        Check whether the cube is solved.

        A face is solved if all 9 stickers on that face have the same color.
        The cube is solved if all faces are solved.
        """
        for stickers in self.faces.values():
            if len(set(stickers)) != 1:
                return False

        return True

    def rotate_face_clockwise(self, face_name):
        """
        Rotate a single face clockwise.

        Index movement:

        Before:
            0 1 2
            3 4 5
            6 7 8

        After clockwise rotation:
            6 3 0
            7 4 1
            8 5 2
        """
        face = self.faces[face_name]

        self.faces[face_name] = [
            face[6], face[3], face[0],
            face[7], face[4], face[1],
            face[8], face[5], face[2],
        ]

    def move_U(self):
        """
        Perform the U move.

        U means rotating the upper face clockwise.

        This affects:
        - The U face itself
        - The top rows of F, L, B, R faces

        With our face orientation:
            F top -> L top
            L top -> B top
            B top -> R top
            R top -> F top
        """
        self.rotate_face_clockwise("U")

        front_top = self.faces["F"][0:3]
        right_top = self.faces["R"][0:3]
        back_top = self.faces["B"][0:3]
        left_top = self.faces["L"][0:3]

        self.faces["L"][0:3] = front_top
        self.faces["B"][0:3] = left_top
        self.faces["R"][0:3] = back_top
        self.faces["F"][0:3] = right_top

    
    def move_U_prime(self):
        """
        Perform the U' move.

        U' means rotating the upper face counter-clockwise.

        Instead of writing separate counter-clockwise logic,
        we perform the U move three times.

        Because:
            U' = U + U + U
        """
        self.move_U()
        self.move_U()
        self.move_U()

    def move_U2(self):
        """
        Perform the U2 move.

        U2 means rotating the upper face twice.

        Because:
            U2 = U + U
        """
        self.move_U()
        self.move_U()

    def move_R(self):
        """
        Perform the R move.

        R means rotating the right face clockwise.

        This affects:
        - The R face itself
        - The right column of U, F, D
        - The left column of B

        With our face orientation:
            F right -> U right
            U right -> B left
            B left  -> D right
            D right -> F right
        """
        self.rotate_face_clockwise("R")

        up_right = [
            self.faces["U"][2],
            self.faces["U"][5],
            self.faces["U"][8],
        ]

        front_right = [
            self.faces["F"][2],
            self.faces["F"][5],
            self.faces["F"][8],
        ]

        down_right = [
            self.faces["D"][2],
            self.faces["D"][5],
            self.faces["D"][8],
        ]

        back_left = [
            self.faces["B"][6],
            self.faces["B"][3],
            self.faces["B"][0],
        ]

        self.faces["U"][2] = front_right[0]
        self.faces["U"][5] = front_right[1]
        self.faces["U"][8] = front_right[2]

        self.faces["B"][6] = up_right[0]
        self.faces["B"][3] = up_right[1]
        self.faces["B"][0] = up_right[2]

        self.faces["D"][2] = back_left[0]
        self.faces["D"][5] = back_left[1]
        self.faces["D"][8] = back_left[2]

        self.faces["F"][2] = down_right[0]
        self.faces["F"][5] = down_right[1]
        self.faces["F"][8] = down_right[2]

    def move_R_prime(self):
        """
        Perform the R' move.

        R' means rotating the right face counter-clockwise.

        Because:
            R' = R + R + R
        """
        self.move_R()
        self.move_R()
        self.move_R()

    def move_R2(self):
        """
        Perform the R2 move.

        R2 means rotating the right face twice.

        Because:
            R2 = R + R
        """
        self.move_R()
        self.move_R()

    def move_F(self):
        """
        Perform the F move.

        F means rotating the front face clockwise.

        This affects:
        - The F face itself
        - The bottom row of U
        - The left column of R
        - The top row of D
        - The right column of L
        """
        self.rotate_face_clockwise("F")

        up_bottom = [
            self.faces["U"][6],
            self.faces["U"][7],
            self.faces["U"][8],
        ]

        right_left = [
            self.faces["R"][0],
            self.faces["R"][3],
            self.faces["R"][6],
        ]

        down_top = [
            self.faces["D"][0],
            self.faces["D"][1],
            self.faces["D"][2],
        ]

        left_right = [
            self.faces["L"][2],
            self.faces["L"][5],
            self.faces["L"][8],
        ]

        self.faces["R"][0] = up_bottom[0]
        self.faces["R"][3] = up_bottom[1]
        self.faces["R"][6] = up_bottom[2]

        self.faces["D"][0] = right_left[2]
        self.faces["D"][1] = right_left[1]
        self.faces["D"][2] = right_left[0]

        self.faces["L"][2] = down_top[0]
        self.faces["L"][5] = down_top[1]
        self.faces["L"][8] = down_top[2]

        self.faces["U"][6] = left_right[2]
        self.faces["U"][7] = left_right[1]
        self.faces["U"][8] = left_right[0]

    def move_F_prime(self):
        """
        Perform the F' move.

        F' means rotating the front face counter-clockwise.

        Because:
            F' = F + F + F
        """
        self.move_F()
        self.move_F()
        self.move_F()

    def move_F2(self):
        """
        Perform the F2 move.

        F2 means rotating the front face twice.

        Because:
            F2 = F + F
        """
        self.move_F()
        self.move_F()

    def move_D(self):
        """
        Perform the D move.

        D means rotating the down face clockwise.

        This affects:
        - The D face itself
        - The bottom rows of F, R, B, L faces

        With our face orientation:
            F bottom -> R bottom
            R bottom -> B bottom
            B bottom -> L bottom
            L bottom -> F bottom
        """
        self.rotate_face_clockwise("D")

        front_bottom = self.faces["F"][6:9]
        right_bottom = self.faces["R"][6:9]
        back_bottom = self.faces["B"][6:9]
        left_bottom = self.faces["L"][6:9]

        self.faces["R"][6:9] = front_bottom
        self.faces["B"][6:9] = right_bottom
        self.faces["L"][6:9] = back_bottom
        self.faces["F"][6:9] = left_bottom
        
    def move_D_prime(self):
        """
        Perform the D' move.

        D' means rotating the down face counter-clockwise.

        Because:
            D' = D + D + D
        """
        self.move_D()
        self.move_D()
        self.move_D()

    def move_D2(self):
        """
        Perform the D2 move.

        D2 means rotating the down face twice.

        Because:
            D2 = D + D
        """
        self.move_D()
        self.move_D()

    def move_L(self):
        """
        Perform the L move.

        L means rotating the left face clockwise.

        This affects:
        - The L face itself
        - The left column of U, F, D
        - The right column of B

        With our face orientation:
            U left  -> F left
            F left  -> D left
            D left  -> B right
            B right -> U left
        """
        self.rotate_face_clockwise("L")

        up_left = [
            self.faces["U"][0],
            self.faces["U"][3],
            self.faces["U"][6],
        ]

        front_left = [
            self.faces["F"][0],
            self.faces["F"][3],
            self.faces["F"][6],
        ]

        down_left = [
            self.faces["D"][0],
            self.faces["D"][3],
            self.faces["D"][6],
        ]

        back_right = [
            self.faces["B"][8],
            self.faces["B"][5],
            self.faces["B"][2],
        ]

        self.faces["F"][0] = up_left[0]
        self.faces["F"][3] = up_left[1]
        self.faces["F"][6] = up_left[2]

        self.faces["D"][0] = front_left[0]
        self.faces["D"][3] = front_left[1]
        self.faces["D"][6] = front_left[2]

        self.faces["B"][8] = down_left[0]
        self.faces["B"][5] = down_left[1]
        self.faces["B"][2] = down_left[2]

        self.faces["U"][0] = back_right[0]
        self.faces["U"][3] = back_right[1]
        self.faces["U"][6] = back_right[2]

    def move_L_prime(self):
        """
        Perform the L' move.

        L' means rotating the left face counter-clockwise.

        Because:
            L' = L + L + L
        """
        self.move_L()
        self.move_L()
        self.move_L()

    def move_L2(self):
        """
        Perform the L2 move.

        L2 means rotating the left face twice.

        Because:
            L2 = L + L
        """
        self.move_L()
        self.move_L()

    def move_B(self):
        """
        Perform the B move.

        B means rotating the back face clockwise.

        This affects:
        - The B face itself
        - The top row of U
        - The right column of R
        - The bottom row of D
        - The left column of L

        With our face orientation:
            R right -> U top
            U top   -> L left
            L left  -> D bottom
            D bottom -> R right
        """
        self.rotate_face_clockwise("B")

        up_top = [
            self.faces["U"][0],
            self.faces["U"][1],
            self.faces["U"][2],
        ]

        right_right = [
            self.faces["R"][2],
            self.faces["R"][5],
            self.faces["R"][8],
        ]

        down_bottom = [
            self.faces["D"][6],
            self.faces["D"][7],
            self.faces["D"][8],
        ]

        left_left = [
            self.faces["L"][0],
            self.faces["L"][3],
            self.faces["L"][6],
        ]

        self.faces["U"][0] = right_right[0]
        self.faces["U"][1] = right_right[1]
        self.faces["U"][2] = right_right[2]

        self.faces["L"][6] = up_top[0]
        self.faces["L"][3] = up_top[1]
        self.faces["L"][0] = up_top[2]

        self.faces["D"][6] = left_left[0]
        self.faces["D"][7] = left_left[1]
        self.faces["D"][8] = left_left[2]

        self.faces["R"][8] = down_bottom[0]
        self.faces["R"][5] = down_bottom[1]
        self.faces["R"][2] = down_bottom[2]

    def move_B_prime(self):
        """
        Perform the B' move.

        B' means rotating the back face counter-clockwise.

        Because:
            B' = B + B + B
        """
        self.move_B()
        self.move_B()
        self.move_B()

    def move_B2(self):
        """
        Perform the B2 move.

        B2 means rotating the back face twice.

        Because:
            B2 = B + B
        """
        self.move_B()
        self.move_B()

    def apply_move(self, move):
        """
        Apply a move to the cube.

        Supported moves:
            U, U', U2
            R, R', R2
            F, F', F2
            D, D', D2
            L, L', L2
            B, B', B2
        """
        if move == "U":
            self.move_U()
        elif move == "U'":
            self.move_U_prime()
        elif move == "U2":
            self.move_U2()
        elif move == "R":
            self.move_R()
        elif move == "R'":
            self.move_R_prime()
        elif move == "R2":
            self.move_R2()
        elif move == "F":
            self.move_F()
        elif move == "F'":
            self.move_F_prime()
        elif move == "F2":
            self.move_F2()
        elif move == "D":
            self.move_D()
        elif move == "D'":
            self.move_D_prime()
        elif move == "D2":
            self.move_D2()
        elif move == "L":
            self.move_L()
        elif move == "L'":
            self.move_L_prime()
        elif move == "L2":
            self.move_L2()
        elif move == "B":
            self.move_B()
        elif move == "B'":
            self.move_B_prime()
        elif move == "B2":
            self.move_B2()
        else:
            raise ValueError(f"Unsupported move: {move}")
        
    def apply_algorithm(self, moves):
        """
        Apply a sequence of moves to the cube.

        Example:
            cube.apply_algorithm(["U", "U'", "U2"])
        """
        for move in moves:
            self.apply_move(move)

    def get_state_string(self):
        """
        Convert the cube state into a single string.

        This is useful for comparing cube states later
        when we write search algorithms.

        Face order:
            U, D, F, B, R, L
        """
        state = ""

        for face_name in ["U", "D", "F", "B", "R", "L"]:
            state += "".join(self.faces[face_name])

        return state
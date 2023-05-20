import tkinter as tk
import numpy as np
import utils

def stoi(s):
    if ((s[0] >= '0' and s[0] <= '9') or s[0] == '-'):
        return int(s)
    return s


def calculate():
    z_entry.delete(0, tk.END)
    solution_entry.delete(0, tk.END)
    # Lấy giá trị từ các đối tượng nhập liệu
    objectives = objective_entry.get().strip()
    constraints = constrain_entry.get().strip()
    conditions = condition_entry.get().strip()

    objectives = np.array([objectives.split(" ")], dtype=object)
    for i in range(len(objectives[0])):
        objectives[0][i] = stoi(objectives[0][i])

    constraints = constraints.split(',')
    constraint_list = []
    for i in constraints:
        constraint_list.append(np.array(i.strip().split(" "), dtype=object))
    constraint_list = np.array(constraint_list, dtype=object)
    for i in range(len(constraint_list)):
        for j in range(len(constraint_list[0])):
            constraint_list[i][j] = stoi(constraint_list[i][j])

    conditions = np.array(conditions.split(" "), dtype=object)
    identity_matrix = np.identity(len(conditions), dtype=object).tolist()
    for i in range(len(conditions)):
        identity_matrix[i].append(conditions[i])
        identity_matrix[i].append(0)
    conditions = np.array(identity_matrix, dtype=object)

    objectives, constraints, conditions = utils.check_condition(objectives, constraint_list, conditions)
    objectives, constraints, conditions = utils.check_constraint(objectives, constraints, conditions)
    objectives, constraints, conditions = utils.check_objective(objectives, constraints, conditions)
   
   
    c = np.array(objectives[0][1:].tolist())
    A = np.array(constraints[:, :-2].tolist())
    b = np.array(constraints[:, -1].tolist())

    b = b.astype(np.float64)
    print(b.dtype)
    print(A, b, c)

    z, solution = utils.two_phases(A, b, c)
    if z == None:
        z_entry.insert(0, "Không có nghiệm")
        solution_entry.insert(0, str("Không có nghiệm"))
    elif z == -np.inf :
        z_entry.insert(0, str("vô số"))
        solution_entry.insert(0, str("vô số"))
    else:
        z_entry.insert(0, str(z))
        solution_entry.insert(0, str(solution))
    



# Tạo một đối tượng Tkinter window
window = tk.Tk()
window.title("Giải Bài toán quy hoạch tuyến tính")

# Tạo một khung nhập liệu
entry_frame = tk.Frame(window, padx=10, pady=10)
entry_frame.pack(side=tk.LEFT, padx=5, pady=5)

objective_label = tk.Label(entry_frame, text="Objective", font=30)
objective_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

objective_entry = tk.Entry(entry_frame, width=80, font=30)
objective_entry.grid(row=0, column=1, padx=5, pady=5)

# Tạo một nhãn cho khung nhập liệu tháng
constrain_label = tk.Label(entry_frame, text="constraints", font=30)
constrain_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

# Tạo một đối tượng nhập liệu tháng
constrain_entry = tk.Entry(entry_frame, width=80, font=30)
constrain_entry.grid(row=1, column=1, padx=5, pady=5)

# Tạo một nhãn cho khung nhập liệu số kw cũ
condition_label = tk.Label(entry_frame, text="Conditions", font=30)
condition_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

# Tạo một đối tượng nhập liệu số kw cũ
condition_entry = tk.Entry(entry_frame, width=80, font=30)
condition_entry.grid(row=2, column=1, padx=5, pady=5)

# Tạo một nút tính toán
calculate_button = tk.Button(entry_frame, text="Calculate",font=30, command=calculate)
calculate_button.grid(row=3, column=1, padx=0, pady=0)


z_label = tk.Label(entry_frame, text="Z = ", font=30)
z_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

z_entry = tk.Entry(entry_frame, width=80, font=30)
z_entry.grid(row=4, column=1, padx=5, pady=5)

solution_label = tk.Label(entry_frame, text="Solution = ", font=30)
solution_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

solution_entry = tk.Entry(entry_frame, width=80, font=30)
solution_entry.grid(row=5, column=1, padx=5, pady=5)


objective_entry.insert(0, str("min -2 6 0"))
condition_entry.insert(0, str(">= >= >="))
constrain_entry.insert(0, str("-1 -1 -1 <= -2, 2 -1 1 <= 1"))
# Chạy vòng lặp chính của ứng dụng
window.mainloop()

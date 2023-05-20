import numpy as np
import pandas as pd

def check_condition(objective, constraint, condition):
    
    condition2=condition
    flag1=0
    flag2=0
    flag3=0
    for i in range(condition2.shape[0]):
        for j in range(condition2.shape[1]):
            if np.diag(condition2)[i] == 1:
                if condition2[i][j] == '<='and condition2[:,-1][i] == 0  :
                    objective[:,i+1+flag2] = objective[:,i+1+flag2]*-1
                    constraint[:,i+flag2]=constraint[:,i+flag2]*-1
                    condition[i][j] = '>='
                    flag1=flag1+1
                elif condition2[i][j] == '>='and condition2[:,-1][i] == 0  :
                    flag3=flag3+1
                elif condition[:,-1][i] != 0 :
                    temp_objective=pd.DataFrame(objective)
                    newcol=np.vstack([temp_objective.iloc[:,2*i+1-flag1-flag3],temp_objective.iloc[:,2*i+1-flag1-flag3]*-1])
                    temp_objective.insert(2*i+1-flag1-flag3,None,newcol[0].T)
                    temp_objective.insert(2*i+2-flag1-flag3,None,newcol[1].T)
                    temp_objective.drop(labels=2*i+1-flag1-flag3,axis=1,inplace=True)
                    objective=temp_objective
                    objective=temp_objective.values
                    
                    temp_constraint=pd.DataFrame(constraint)
                    newrow=np.zeros(temp_constraint.shape[1],dtype=np.object)
                    newrow[i-flag1-flag3:]=condition2[i,:]                    
                    temp_constraint.loc[temp_constraint.shape[0]+1]=newrow
                    #constraint= np.vstack([constraint, newrow])
                    newcol=np.vstack([temp_constraint.iloc[:,2*i-flag1-flag3],temp_constraint.iloc[:,2*i-flag1-flag3]*-1])
                    temp_constraint.insert(2*i-flag1-flag3,None,newcol[0].T)
                    temp_constraint.insert(2*i+1-flag1-flag3,None,newcol[1].T)
                    temp_constraint.drop(labels=2*i-flag1-flag3,axis=1,inplace=True)
                    constraint=temp_constraint.values
                    
                    
                    newcol=np.zeros(condition.shape[0],dtype=np.object)
                    newrow=np.zeros(condition.shape[1]+1,dtype=np.object)
                    temp_condition=pd.DataFrame(condition)
                    temp_condition.insert(condition.shape[1]-2,None,newcol.T)
                    temp_condition.loc[condition.shape[0]]=newrow
                    temp_condition.iloc[-1,condition.shape[1]-1]='>='
                    temp_condition.iloc[-1,condition.shape[1]-2]=1
                    temp_condition.iloc[i,condition.shape[1]]=0
                    temp_condition.iloc[i,condition.shape[1]-1]='>='
                    condition = np.array(temp_condition)
                    
                    flag2=flag2+1
                elif condition2[i][j] == '?'and condition2[:,-1][i] == 0:
                    temp_objective=pd.DataFrame(objective)
                    newcol=np.vstack([temp_objective.iloc[:,2*i+1-flag1-flag3],temp_objective.iloc[:,2*i+1-flag1-flag3]*-1])
                    temp_objective.insert(2*i+1-flag1-flag3,None,newcol[0].T)
                    temp_objective.insert(2*i+2-flag1-flag3,None,newcol[1].T)
                    temp_objective.drop(labels=2*i+1-flag1-flag3,axis=1,inplace=True)
                    objective=temp_objective
                    objective=temp_objective.values
                    
                    temp_constraint=pd.DataFrame(constraint)
                    
                    #constraint= np.vstack([constraint, newrow])
                    newcol=np.vstack([temp_constraint.iloc[:,2*i-flag1-flag3],temp_constraint.iloc[:,2*i-flag1-flag3]*-1])
                    temp_constraint.insert(2*i-flag1-flag3,None,newcol[0].T)
                    temp_constraint.insert(2*i+1-flag1-flag3,None,newcol[1].T)
                    temp_constraint.drop(labels=2*i-flag1-flag3,axis=1,inplace=True)
                    constraint=temp_constraint.values
                    
                    
                    newcol=np.zeros(condition.shape[0],dtype=np.object)
                    newrow=np.zeros(condition.shape[1]+1,dtype=np.object)
                    temp_condition=pd.DataFrame(condition)
                    temp_condition.insert(condition.shape[1]-2,None,newcol.T)
                    temp_condition.loc[condition.shape[0]]=newrow
                    temp_condition.iloc[-1,condition.shape[1]-1]='>='
                    temp_condition.iloc[-1,condition.shape[1]-2]=1
                    temp_condition.iloc[i,condition.shape[1]]=0
                    temp_condition.iloc[i,condition.shape[1]-1]='>='
                    condition = np.array(temp_condition)
                    
                    flag2=flag2+1
                
    return objective,constraint,condition

def check_constraint(objective, constraint, condition):
    constraint2=constraint
    k=constraint.shape[1]-2
    flag=0
    for i in range(constraint2.shape[0]):
        if constraint[i-flag][k] == ">=":
            constraint[i-flag,:]=constraint[i-flag,:]*-1
            constraint[i-flag][k] = "<="
            
        if constraint2[:,k][i] == "=":
            newrow=np.vstack([constraint[i-flag],constraint[i-flag]*-1])
            newrow[0][k]='<='
            newrow[1][k]='<='
            temp_constraint=pd.DataFrame(constraint)
            #temp_constraint = temp_constraint.drop(labels=i, axis=0)
            temp_constraint.loc[temp_constraint.shape[0]+1]=newrow[0]
            temp_constraint.loc[temp_constraint.shape[0]+2]=newrow[1]
            temp_constraint = temp_constraint.drop(labels=i-flag, axis=0)
            flag=flag+1
                    
            constraint=temp_constraint.values
    return objective,constraint,condition

def check_objective(objective, constraint, condition):
    if objective[0][0]=='max':
        objective=objective*-1
        objective[0][0]='min'
    return objective, constraint, condition


def two_phases(A,b,c):

    m, n = A.shape
    # Khởi tạo biến giá trị tối ưu
    z = 0
    # Tính ma trận bổ sung có chứa x0
    c1 = np.concatenate((np.ones(1), np.zeros(m+n)))
    new_col = (-1*np.ones(m)).reshape(-1, 1)
    T = np.hstack((new_col,np.hstack((A, np.eye(m)))))
    b_n = b.copy()


    # Copy biến ban đầu để so sánh
    A_cop = T.copy()
    c_cop = c1.copy()
    b_cop = b.copy()

    # Tính biến cơ sở ban đầu
    basis = list(range(n+1, n + m+1))
    # Chuyển về dạng chuẩn tắc

    #Chọn biến vào
    j = 0
    #Tìm biến ra
    i = np.argmin(b_n)

    
    # Tính giá trị tối ưu
    z += c1[j] / T[i, j] * b_n[i]
    # Cập nhật ma trận
    basis[i] = j
    
    for k in range(m):
        if k != i:
            b_n[k] -= T[k, j]/T[i,j] * b_n[i]
            T[k, :] -=  T[k, j] / T[i,j] * T[i, :]
    
    b_n[i] /= T[i, j]
    T[i, :] /= T[i, j]       
    c1 -= c1[j] * T[i, :]

    #phase 1
    while True:
        # Tìm biến vào
        j = np.argmin(c1)
        
        if c1[j] >= 0:
            break
            
        # Tìm biến ra
        ratios = [float('inf')] * m
        for i in range(m):
            if T[i, j] > 0:
                ratios[i] = b_n[i] / T[i, j]
        
        i = np.argmin(ratios)

        # Kiểm tra bài toán không giới nội hoặc từ vựng tối ưu
        if ratios[i] == float('inf'):
            return -np.inf, None
        
        # Tính giá trị tối ưu
        z += c1[j] / T[i, j] * b_n[i]
        # Cập nhật ma trận
        basis[i] = j
        
        for k in range(m):
            if k != i:
                b_n[k] -= T[k, j]/T[i,j] * b_n[i]
                T[k, :] -=  T[k, j] / T[i,j] * T[i, :]
        
        b_n[i] /= T[i, j]
        T[i, :] /= T[i, j]       
        c1 -= c1[j] * T[i, :]
        # Kiểm tra thuật toán có hoàn thành hay không 
        # Nếu Từ vựng mới trùng với từ vựng ban đầu thì dừng thuật toán
        if (c1 == c_cop).all() and (T == A_cop).all() and (b_n == b_cop).all():
            print("Thuật toán lặp vô hạn.")
            return None, None
        
    #Kiểm tra bài toán có nghiệm khi hoàn thành phase 1
    if np.array_equal(c1,c_cop) == False:
        return None, None
    #Thiết lập hàm mục tiêu cho phase 2
    # c_n = np.concatenate((np.zeros(len(c)), np.zeros(m)))
    c_n = np.zeros(m+n) # trường hợp các biến trên hàm mục tiêu không đủ

    #loại bỏ x0
    T = T[:, 1:]
    T_z = T.copy()
    for i in range(m):
        if basis[i] <= n:
            T_z[i,basis[i]-1] = 0 # làm mất biến thay vào khi thêm vào hàm mục tiêu
            c_n += c[basis[i]-1] * T_z[i,:] #vì basis có tính 0
            z += c[basis[i]-1] * b_n[i]
    #Cập nhật giá trị z cho phase 2
    c_n *= -1
    #Cập nhật lại basis
    basis -= np.ones(len(basis))
    #phase 2

    while True:
        # Tìm biến vào
        j = np.argmin(c_n)
        
        if c_n[j] >= 0:
            break
            
        # Tìm biến ra
        ratios = [float('inf')] * m
        for i in range(m):
            if T[i, j] > 0:
                ratios[i] = b_n[i] / T[i, j]
        
        i = np.argmin(ratios)

        # Kiểm tra bài toán không giới nội
        if ratios[i] == float('inf'):
            print("Bài toán không giới nội.")
            return -np.inf, None
        
        # Tính giá trị tối ưu
        z += c_n[j] / T[i, j] * b_n[i]
        # Cập nhật ma trận
        basis[i] = j
        
        for k in range(m):
            if k != i:
                # x1 = T[k, j]/T[i,j]
                # x2 = b_n[i]
                # b_n[k] -= np.multiply(x1,x2)
                b_n[k] -= (T[k, j]/T[i,j]) * b_n[i]
                T[k, :] -=  T[k, j] / T[i,j] * T[i, :]
        
        b_n[i] /= T[i, j]
        T[i, :] /= T[i, j]
        c_n -= c_n[j] * T[i, :]
        # Kiểm tra thuật toán có hoàn thành hay không 
        # Nếu Từ vựng mới trùng với từ vựng ban đầu thì dừng thuật toán
        if np.array_equal(c_n, c_cop) and np.array_equal(T, A_cop) and np.array_equal(b_n, b_cop):
            print("Thuật toán lặp vô hạn.")
            # Thêm bland vào đây
            return None, None
        
    # Tìm nghiệm tối ưu
    x = np.zeros(n)
    for i in range(m):
        if basis[i] < n:
            if i <= len(b_n):
                x[int(basis[i])] = b_n[i]
            else:
                x[int(basis[i])] = 0
            # try:
            #     idx = int(basis[i])
            #     if idx < 0 or idx >= len(x):
            #         raise IndexError
            #     x[idx] = b_n[i]
            # except (IndexError, ValueError):
            #     print(f"Invalid basis index at i = {i}")
            #     x[basis[i]] = 0      




    return z, x  
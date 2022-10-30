import os

import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox,filedialog
from socker import SshTest
#创建窗体
root = ttk.Window()
root.title("Linux远程执行工具")
root.iconphoto(False, tk.PhotoImage(file='logo.png'))
root.geometry("320x219")
root.resizable(width=0,height=0)

#函数区

#远程命令提交
def commit():
    if not host_file.get():
        tk.messagebox.showerror('提示','请选择正确的主机文件')
    elif not cmd_file.get():
        tk.messagebox.showerror('提示', '请选择正确的命令文件')
    elif not report_file.get():
        tk.messagebox.showerror('提示', '请选择报告存放路径')
    else:
        with open(host_file.get()) as f:
            for line in f:
                line= line.strip()
                host,port,username,pwd=line.split(':')
                ssh=SshTest(host,port,username,pwd)
                ssh_return=ssh.check_ssh_status()
                print(str(host) + '主机SSH状态为： ' + str(ssh_return[2]) + '\n')
                cmd_info=open(cmd_file.get(),encoding='utf8')
                command=cmd_info.read()
                ssh.exec_ssh_cmd(command,report_file.get())
                ssh.ssh.close()

    tk.messagebox.showinfo("提示","执行完成\n"
                                  "请查看报告文件")

#选择文件函数
def cmd_select_file():
    # 单个文件选择
    selected_file_path = filedialog.askopenfilename(initialdir="./config")  # 使用askopenfilename函数选择单个文件
    cmd_path.set(selected_file_path)

def report_select_file():
    # 单个文件选择
    selected_file_path = filedialog.askdirectory(initialdir="./config/")  # 使用askopenfilename函数选择单个文件
    report_path.set(selected_file_path)

def open_host_file():
    file_path=filedialog.askopenfilenames(initialdir="./config")
    host_path.set(file_path)
def about():
    tk.messagebox.showinfo('关于','描述：Linux远程命令执行工具\n'
                                  '版本：V1.0\n'
                                  '作者：seanchen')
#配置文件管理
def config():
    config_window=ttk.Toplevel(root)
    config_window.geometry("268x245")
    config_window.title("配置文件管理")
    config_window.iconphoto(False, tk.PhotoImage(file='logo.png'))
    filepath='config'
    files = os.listdir(filepath)
    list_file = tk.Listbox(config_window,width=30)
    list_file.pack()

    def delete_file():#删除配置文件
        path=tk.StringVar()
        cu_rels = list_file.curselection()
        if cu_rels !=():
            cur=list_file.selection_get()#获取当前选中的内容
            path.set(cur)#写入当前选中的列表内容到path
            list_file.delete(cu_rels)#删除Listbox列表对应游标的内容
            os.remove(path.get())#删除当前选择的文件
            messagebox.showinfo("提示","删除成功")

    ttk.Button(config_window, text="删除", command=delete_file,width=10).pack(side=tk.LEFT,padx=15)
    ttk.Button(config_window,text="添加配置",command=addconfig_view,width=10).pack(side=tk.LEFT,padx=10)
    #遍历配置文件目录并插入Listbox列表
    for fdi in files:
        f_id=os.path.join(filepath,fdi)
        list_file.insert('end',f_id)



#新建配置文件
def addconfig_view():
    add_config=ttk.Toplevel(root)#新建顶部窗口
    add_config.geometry("640x319") #设置窗口大小
    add_config.resizable(width=0,height=0)#固定窗口大小
    add_config.iconphoto(False, tk.PhotoImage(file='logo.png'))#配置文件图标
    add_config.title("新建配置")
    st = tk.Text(add_config, height=10, )
    st.pack(fill=ttk.BOTH, expand=True)
    def savefile():
        try:
            context=st.get("1.0",'end-1c')
            files = [('All Files', '*.*'),
                     ('Python Files', '*.py'),
                     ('Text Document', '*.txt')]
            filename=filedialog.asksaveasfile(filetypes=files,defaultextension=files,initialdir="./config")
            if not filename.name:
                return
            else:
                with open(filename.name,"w") as f:
                    f.write(context)
        except Exception as e:
            print(e)
        add_config.destroy()
    def cancel_save():
        add_config.destroy()
    ttk.Button(add_config,text="保存",command=savefile,width=20).pack(side=tk.LEFT,fill=ttk.X,padx=80)
    ttk.Button(add_config, text="取消",command=cancel_save,width=20).pack(side=tk.LEFT,fill=ttk.X,padx=20)



#菜单栏
main_menu=ttk.Menu(root)

config_menus=ttk.Menu(main_menu, tearoff=False)
config_menus.add_command(label='管理配置文件',command=config)
config_menus.add_command(label="新建配置",command=addconfig_view)
main_menu.add_cascade(label="配置管理",menu=config_menus)
main_menu.add_command(label='关于',command=about)
# main_menu = tk.Menu(root)  # 创建主菜单
# menu_sub = tk.Menu(main_menu)  # 创建子菜单
# menu_sub.add_command(label='子菜单1', command=lambda x='子菜单1': do(x))  # 一个子菜单
# menu_sub.add_command(label='子菜单2', command=lambda x='子菜单2': do(x))  # 一个子菜单
# menu_sub.add_command(label='子菜单3', command=lambda x='子菜单3': do(x))  # 一个子菜单
# main_menu.add_cascade(label='主菜单', menu=menu_sub)  # 添加子菜单到主菜单
# # root.config(menu=menu_main)


#主窗口
#默认路径
cmd_path=tk.StringVar(value='config/cmd.txt') #脚本默认路径
host_path=tk.StringVar(value='config/host.txt') #主机信息默认路径
report_path=tk.StringVar(value='config/')#巡检报告默认路径
ttk.Label(root,text="主机信息:",padding=10).grid(row=0,column=1)
host_file=ttk.Entry(root,textvariable=host_path)
host_file.grid(row=0,column=2)
ttk.Button(root,text="浏览",bootstyle="success-outline",command=open_host_file).grid(row=0,column=3,padx=5)
ttk.Label(root,text="脚本信息:",padding=10).grid(row=1,column=1)
cmd_file=ttk.Entry(root,textvariable=cmd_path)
cmd_file.grid(row=1,column=2)
ttk.Button(root,text="浏览",bootstyle="success-outline",command=cmd_select_file).grid(row=1,column=3,padx=5)
ttk.Label(root,text="报告信息:",padding=10).grid(row=2,column=1)
report_file=ttk.Entry(root,textvariable=report_path)
report_file.grid(row=2,column=2)
ttk.Button(root,text="浏览",bootstyle="success-outline",command=report_select_file).grid(row=2,column=3,padx=5)
ttk.Button(root,text="开始执行",bootstyle="success",command=commit,width=30).grid(row=5,columnspan=10,padx=20,pady=20)




if __name__=='__main__':
    root.config(menu=main_menu)
    root.mainloop()
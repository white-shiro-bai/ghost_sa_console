# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
import json
from component.ui import ui
from component.public_value import get_time_array_from_nlp

class console:
    def __init__(self):
        from configs import admin
        self.post_data = {'password':admin.admin_password,'mode':'cli'}
        self.domain = admin.domain
        self.menu_history = ['show_home']
    def get_data(self,url,params=None):
        from component.api_req import get_json_from_postdata
        if params:
            for key in params:
                self.post_data[key] = params[key]
        self.json_results = get_json_from_postdata(url=self.domain+url,data=self.post_data)
        return self.json_results

    def project_select(self):
        self.projectslist = self.get_data(url='/show_project_list')
        self.project = ui(data={"desc":"需要选定一个项目以开始运行","type":"option","display_key":"project","func_key":"project","data":self.projectslist["data"]})[0]
        self.post_data["project"] = self.project
        print('选定的project是：',self.project)

    def get_onwer(self):
        self.owner = ui(data={"desc":"需要输入一个用户名用来识别您的身份","type":"keyword","display_key":"用户名","allow_none":False})[0]
        self.post_data["owner"] = self.owner
        print('使用的身份是：',self.owner)

    def play(self):
        self.get_onwer()
        self.project_select()
        self.inited_post = dict(self.post_data)
        self.show_home()

    def show_home(self):
        self.post_data = dict(self.inited_post)
        self.func_home = [{"func_id":1,"func_key":"usergroup","func_name":"用户分群"},{"func_id":2,"func_key":"noti_group","func_name":"推送列表"},{"func_id":3,"func_key":"noti_temple","func_name":"推送模板"},{"func_id":4,"func_key":"scheduler_jobs","func_name":"分群任务列表"},{"func_id":5,"func_key":"create_manual","func_name":"手动执行该分群"}]
        self.func_key = ui(data={"type":"option","display_key":"func_id","func_key":"func_key","data":self.func_home})
        self.menu_history.append(self.func_key[0])
        self.menu()

    def menu(self):
        if self.menu_history[-1] == '~home':
            self.menu_history.pop()
            getattr(self, 'show_home')()
        elif self.menu_history[-1] == '~refresh':
            self.menu_history.pop()
            getattr(self, self.menu_history[-1])()
        elif self.menu_history[-1] == '~back':
            if len(self.menu_history) <= 2 :
                print('已退到顶层')
                self.menu_history.pop()
                getattr(self, self.menu_history[-1])()
            else:
                self.menu_history.pop()
                self.menu_history.pop()
            getattr(self, self.menu_history[-1])()
        else:
            getattr(self, self.menu_history[-1])()

    def usergroup(self):
        while True:
            self.post_data = dict(self.inited_post)
            self.plan = self.get_data(url='/usergroups/show_usergroup_plan')
            self.plan_id = ui(data={"desc":"选择要操作的分群","type":"option","display_key":"plan_id","func_key":"plan_id","data":self.plan["data"]})
            if self.plan_id[1] == '~menu':
                self.menu_history.append(self.plan_id[0])
                self.menu()
            else:
                self.plan_list = self.get_data(url='/usergroups/show_usergroup_list',params={"plan_id":self.plan_id[0]})
                self.list_id = ui(data={"limit_func":True,"desc":"选择要操作的分群里列表","type":"option","display_key":"list_id","func_key":"list_id","data":self.plan_list["data"]})
                self.opt = ui(data={"limit_func":True,"desc":"选择要进行的操作","type":"option","display_key":"func_id","func_key":"func_name","data":[{"func_id":1,"func_name":"apply_temple","func_desc":"应用模板"},{"func_id":2,"func_name":"re_group","func_desc":"重新分群"},{"func_id":3,"func_name":"re_select","func_desc":"重选列表"},{"func_id":4,"func_name":"show_data","func_desc":"查询该列表数据"},{"func_id":5,"func_name":"do_data","func_desc":"选择单条数据执行"}]})
                if self.opt[0] == "re_select":
                    continue
                elif self.opt[0] == "re_group":
                    print(self.get_data(url='/usergroups/duplicate_scheduler_jobs',params={"list_id":self.list_id[0]}))
                    self.menu_history = ['show_home']
                    self.show_home()
                elif self.opt[0] == "apply_temple":
                    self.temple_id_list = self.get_data(url='/usergroups/show_temples')
                    self.temple_id_target = ui(data={"limit_func":True,"desc":"选择要应用的模板id","type":"option","display_key":"temple_id","func_key":"temple_id","data":self.temple_id_list["data"]})
                    self.send_at_str = ui(data={"limit_func":True,"desc":"请输入消息发送的时间，格式 YYYY-MM-DD HH:MM:SS 不输入的话，则为立即发送","type":"keyword","display_key":"发送时间","allow_none":True})[0]
                    if self.send_at_str and self.send_at_str != '':
                        self.send_at_int = get_time_array_from_nlp(self.send_at_str)['time_int']
                        print(self.get_data(url='/usergroups/apply_temples_list',params={"temple_id":self.temple_id_target[0],"user_group_id":self.list_id[0],"owner":self.owner,"send_at":self.send_at_int}))
                    else:
                        print(self.get_data(url='/usergroups/apply_temples_list',params={"temple_id":self.temple_id_target[0],"user_group_id":self.list_id[0],"owner":self.owner}))
                    self.menu_history = ['show_home']
                    self.show_home()
                elif self.opt[0] == "show_data":
                    self.everywhere = ui(data={"limit_func":True,"desc":"请输入查询条件，留空则查询全部","type":"keyword","display_key":"全文关键词","allow_none":True})[0]
                    self.list_data = self.get_data(url='/usergroups/show_usergroup_data',params={'list_id':self.list_id,'everywhere':self.everywhere})
                    ui(data={"limit_func":True,"desc":"该分组列表下的数据为","type":"show","data":self.list_data["data"]})
                elif self.opt[0] == "do_data":
                    self.everywhere = ui(data={"limit_func":True,"desc":"请输入查询条件，留空则查询全部","type":"keyword","display_key":"全文关键词","allow_none":True})[0]
                    self.list_data = self.get_data(url='/usergroups/show_usergroup_data',params={'list_id':self.list_id,'everywhere':self.everywhere})
                    self.data_selected = ui(data={"limit_func":True,"desc":"该分组列表下的数据为","type":"option","display_key":"data_id","func_key":"data_id","data":self.list_data["data"]})[0]
                    self.opt = ui(data={"limit_func":True,"desc":"选择要进行的操作","type":"option","display_key":"func_id","func_key":"func_name","data":[{"func_id":1,"func_name":"apply_temple","func_desc":"应用模板"},{"func_id":2,"func_name":"disable","func_desc":"禁用该数据"},{"func_id":3,"func_name":"re_select","func_desc":"重选列表"}]})
                    if self.opt[0] == "re_select":
                        continue
                    elif self.opt[0] == "disable":
                        print(self.get_data(url='/usergroups/disable_usergroup_data',params={'list_id':self.list_id,'data_id':self.data_selected}))
                        self.menu_history = ['show_home']
                        self.show_home()
                    elif self.opt[0] == "apply_temple":
                        self.temple_id_list = self.get_data(url='/usergroups/show_temples')
                        self.temple_id_target = ui(data={"limit_func":True,"desc":"选择要应用的模板id","type":"option","display_key":"temple_id","func_key":"temple_id","data":self.temple_id_list["data"]})
                        self.send_at_str = ui(data={"limit_func":True,"desc":"请输入消息发送的时间，格式 YYYY-MM-DD HH:MM:SS 不输入的话，则为立即发送","type":"keyword","display_key":"发送时间","allow_none":True})[0]
                        if self.send_at_str and self.send_at_str != '':
                            self.send_at_int = get_time_array_from_nlp(self.send_at_str)['time_int']
                            print(self.get_data(url='/usergroups/apply_temples_list',params={"temple_id":self.temple_id_target[0],"data_id":self.data_selected,"owner":self.owner,"send_at":self.send_at_int}))
                        else:
                            print(self.get_data(url='/usergroups/apply_temples_list',params={"temple_id":self.temple_id_target[0],"data_id":self.data_selected,"owner":self.owner}))
                        self.menu_history = ['show_home']
                        self.show_home()

    def create_manual(self):
        while True:
            self.post_data = dict(self.inited_post)
            self.plan = self.get_data(url='/usergroups/show_usergroup_plan')
            self.plan_id = ui(data={"desc":"选择要操作的分群","type":"option","display_key":"plan_id","func_key":"plan_id","data":self.plan["data"]})
            if self.plan_id[1] == '~menu':
                self.menu_history.append(self.plan_id[0])
                self.menu()
            else:
                self.send_at_str = ui(data={"limit_func":True,"desc":"请输入分群执行的时间，格式 YYYY-MM-DD HH:MM:SS 不输入的话，则为立即发送","type":"keyword","display_key":"发送时间","allow_none":True})[0]
                if self.send_at_str and self.send_at_str != '':
                    self.send_at_int = get_time_array_from_nlp(self.send_at_str)['time_int']
                    print(self.get_data(url='/usergroups/create_scheduler_jobs_manual',params={'plan_id':self.plan_id,"send_at":self.send_at_int}))
                else:
                    print(self.get_data(url='/usergroups/create_scheduler_jobs_manual',params={'plan_id':self.plan_id}))
                self.menu_history = ['show_home']
                self.show_home()

    def noti_group(self):
        while True:
            self.post_data = dict(self.inited_post)
            self.noti_group_list = self.get_data(url='/usergroups/show_noti_group')
            self.noti_group_id = ui(data={"desc":"选择要操作的推送组","type":"option","display_key":"noti_group_id","func_key":"noti_group_id","data":self.noti_group_list["data"]})
            if self.noti_group_id[1] == '~menu':
                self.menu_history.append(self.noti_group_id[0])
                self.menu()
            else:
                self.opt = ui(data={"limit_func":True,"desc":"选择要进行的操作","type":"option","display_key":"func_id","func_key":"func_name","data":[{"func_id":1,"func_name":"send_group","func_desc":"推送该推送组除单条禁用外的全部消息"},{"func_id":2,"func_name":"group_detial","func_desc":"查询该推送组的内容"},{"func_id":3,"func_name":"re_select","func_desc":"重选列表"},{"func_id":4,"func_name":"do_detail","func_desc":"选择单条推送执行"}]})
                if self.opt[0] == "re_select":
                    continue
                elif self.opt[0] == "group_detial":
                    # self.everywhere = ui(data={"limit_func":True,"desc":"请输入查询条件，留空则查询全部","type":"keyword","display_key":"全文关键词","allow_none":True})[0]
                    self.list_data = self.get_data(url='/usergroups/show_noti_detial',params={'noti_group_id':self.noti_group_id[0]})
                    ui(data={"limit_func":True,"desc":"该分组列表下的数据为","type":"show","data":self.list_data["data"]})
                elif self.opt[0] == "send_group":
                    print(self.get_data(url='/usergroups/manual_send',params={"noti_group_id":self.noti_group_id[0]}))
                    continue
                elif self.opt[0] == "do_detail":
                    # self.everywhere = ui(data={"limit_func":True,"desc":"请输入查询条件，留空则查询全部","type":"keyword","display_key":"全文关键词","allow_none":True})[0]
                    self.list_data = self.get_data(url='/usergroups/show_noti_detial',params={'noti_group_id':self.noti_group_id[0]})
                    self.noti = ui(data={"limit_func":True,"desc":"选择需要操作的信息","type":"option","display_key":"noti_id","func_key":"noti_id","data":self.list_data["data"]})
                    self.opt = ui(data={"limit_func":True,"desc":"选择要进行的操作","type":"option","display_key":"func_id","func_key":"func_name","data":[{"func_id":1,"func_name":"send_detial","func_desc":"发送"},{"func_id":2,"func_name":"disable","func_desc":"禁用该数据"},{"func_id":3,"func_name":"re_select","func_desc":"重选列表"}]})
                    if self.opt[0] == "re_select":
                        continue
                    elif self.opt[0] == 'disable':
                        print(self.get_data(url='/usergroups/disable_single_noti',params={"noti_id":self.noti[0]}))
                        continue
                    elif self.opt[0] == 'send_detial':
                        print(self.get_data(url='/usergroups/manual_send',params={"noti_id":self.noti[0]}))
                        continue

    def noti_temple(self):
        self.post_data = dict(self.inited_post)
        self.temple_id_list = self.get_data(url='/usergroups/show_temples')
        print(ui(data={"limit_func":False,"desc":"当前可用的模板","type":"show","display_key":"temple_id","func_key":"temple_id","data":self.temple_id_list["data"]}))
        self.menu_history.pop()
        self.menu()

    def scheduler_jobs(self):
        self.post_data = dict(self.inited_post)
        self.scheduler_jobs_list = self.get_data(url='/usergroups/show_scheduler_jobs')
        print(ui(data={"limit_func":False,"desc":"当前分群队列","type":"show","display_key":"temple_id","func_key":"temple_id","data":self.scheduler_jobs_list["data"]}))
        self.menu_history.pop()
        self.menu()

if __name__ == "__main__":
    v = console()
    v.play()
from threading import Timer
from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from generic_resources.views import update_flavor_data, update_image_data
from teacher.infra_generator import big_bang, big_crunch

from teacher.models import Cloudinfra, Network, Router, Server, Teacher


class CloudinfraListView(ListView):
    model = Cloudinfra
    fields = ['infra_name', 'minutes_to_live',]
    template_name = 'teacher/resource_list.html'
    
    def get_queryset(self):
        teacher = Teacher.objects.get(pk=self.kwargs['pk'])
        queryset =  Cloudinfra.objects.filter(teacher=teacher)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher'] = Teacher.objects.get(pk=self.kwargs['pk'])
        return context


class CloudinfraCreateView(CreateView):
    model = Cloudinfra
    fields = ['infra_name', 'minutes_to_live']
    template_name = 'teacher/partials/resource_create.html'

    def get_success_url(self):
        return reverse_lazy('teacher:infra-list', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        teacher = Teacher.objects.get(pk=self.kwargs['pk'])
        form.instance.teacher = teacher
        response_received = super().form_valid(form)
        cloudinfra = Cloudinfra.objects.get(pk=form.instance.id)
        router = Router.objects.create(router_name="Public Network Router", cloudinfra=cloudinfra)
        Network.objects.create(network_name="Public Network", network_cidr="Default", router=router, cloudinfra=cloudinfra)
        return response_received

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_type'] = "none"
        return context


class CloudinfraDeleteView(DeleteView):
    model = Cloudinfra

    def get_object(self, queryset=None):
      pk = self.kwargs['pk2']
      return self.get_queryset().filter(pk=pk).get()
    
    def get_success_url(self):
        return reverse_lazy('teacher:infra-list', kwargs={'pk': self.kwargs['pk']})


class CloudinfraDetailView(DetailView):
    model = Cloudinfra
    fields = ['infra_name']
    template_name = 'teacher/resource_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher'] = Teacher.objects.get(pk=self.kwargs['pk'])
        context['routers'] = Router.objects.filter(cloudinfra = context['object'])
        context['networks'] = Network.objects.filter(cloudinfra = context['object'])
        context['servers'] = Server.objects.filter(cloudinfra = context['object'])
        return context

    def get_object(self, queryset=None):
      pk = self.kwargs['pk2']
      teacher = Teacher.objects.get(pk=self.kwargs['pk'])
      return self.get_queryset().filter(pk=pk, teacher=teacher).get()
    

class RouterCreateView(CreateView):
    model = Router
    fields = ['router_name']
    template_name = 'teacher/partials/resource_create.html'

    def get_success_url(self):
        return reverse_lazy('teacher:infra-detail', kwargs={'pk': self.kwargs['pk'], 'pk2': self.kwargs['pk2']})

    def form_valid(self, form):
        cloudinfra = Cloudinfra.objects.get(pk=self.kwargs['pk2'])
        form.instance.cloudinfra = cloudinfra
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_type'] = "router"
        return context


class NetworkCreateView(CreateView):
    model = Network
    fields = ['network_name', 'network_cidr', 'router']
    template_name = 'teacher/partials/resource_create.html'

    def get_success_url(self):
        return reverse_lazy('teacher:infra-detail', kwargs={'pk': self.kwargs['pk'], 'pk2': self.kwargs['pk2']})

    def form_valid(self, form):
        cloudinfra = Cloudinfra.objects.get(pk=self.kwargs['pk2'])
        form.instance.cloudinfra = cloudinfra
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        cloudinfra = Cloudinfra.objects.get(pk=self.kwargs['pk2'])
        context = super().get_context_data(**kwargs)
        empty_tuple = ("", "None")  
        choice_list = []
        choice_list.append(empty_tuple)
        for router in Router.objects.filter(cloudinfra=cloudinfra):
            resource_id = str(router.id)
            resource_tuple = (resource_id, router.router_name)
            choice_list.append(resource_tuple)
        context['form'].fields['router'].choices = choice_list
        context['resource_type'] = "network"
        return context


class ServerCreateView(CreateView):
    model = Server
    fields = ['server_name', 'image', 'flavor', 'network', 'floating_ip', 'server_status']
    template_name = 'teacher/partials/resource_create.html'

    def get_success_url(self):
        return reverse_lazy('teacher:infra-detail', kwargs={'pk': self.kwargs['pk'], 'pk2': self.kwargs['pk2']})

    def form_valid(self, form):
        cloudinfra = Cloudinfra.objects.get(pk=self.kwargs['pk2'])
        form.instance.cloudinfra = cloudinfra
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cloudinfra = Cloudinfra.objects.get(pk=self.kwargs['pk2'])
        context['form'].fields['image'] = forms.ChoiceField(choices=update_image_data())
        context['form'].fields['flavor'] = forms.ChoiceField(choices=update_flavor_data())
        empty_tuple = ("", "None")  
        choice_list = []
        choice_list.append(empty_tuple)
        for network in Network.objects.filter(cloudinfra=cloudinfra):
            resource_id = str(network.id)
            resource_tuple = (resource_id, network.network_name)
            choice_list.append(resource_tuple)
        context['form'].fields['network'].choices = choice_list
        context['resource_type'] = "server"
        return context




def buildInfra(request, pk, pk2):
    cloudinfra = Cloudinfra.objects.get(pk=pk2)
    labels_dict = {
        "resource_type": "resource",
        "resource_detail": "details",
        "network_name": "network_name",
        "network_cidr": "subnet_cidr",
        "router_name": "router_name",
        "router_external_gateway": "external_gateway",
        "router_internal_interface": "internal_interface",
        "server_name": "server_name",
        "image_name": "image_name",
        "flavor_name": "flavor_name",
        "floating_ip": "floating_ip",
        "server_status": "status",
    }

    resource_list = []


    # For Networks
    temp_main_dict = {}
    temp_main_dict[labels_dict['resource_type']] = "network"
    temp_list = []
    for network in Network.objects.filter(cloudinfra=cloudinfra):
        temp_sub_dict = {}

        if network.network_name == "Public Network":
            pass
        else:
            temp_sub_dict[labels_dict['network_name']] = network.network_name
            temp_sub_dict[labels_dict['network_cidr']] = network.network_cidr
            
        if bool(temp_sub_dict):
            temp_list.append(temp_sub_dict)
    temp_main_dict[labels_dict['resource_detail']] = temp_list
    resource_list.append(temp_main_dict)


    # For Routers
    temp_main_dict = {}
    temp_main_dict[labels_dict['resource_type']] = "router"
    temp_list = []


    for router in Router.objects.filter(cloudinfra=cloudinfra):
        temp_sub_dict = {}

        if router.router_name == "Public Network Router":
            temp_sub_dict[labels_dict['router_name']] = "public_router"
            temp_sub_dict[labels_dict['router_external_gateway']] = True
            networkList = []
            for network in Network.objects.filter(router=router):
                if network.network_name == "Public Network":
                    pass
                else:
                    networkList.append(network.network_name)
            temp_sub_dict[labels_dict['router_internal_interface']] = networkList
        else:
            temp_sub_dict[labels_dict['router_name']] = router.router_name
            temp_sub_dict[labels_dict['router_external_gateway']] = False            
            networkList = []
            for network in Network.objects.filter(router=router):
                networkList.append(network.network_name)
            temp_sub_dict[labels_dict['router_internal_interface']] = networkList

        if bool(temp_sub_dict):
            temp_list.append(temp_sub_dict)
    temp_main_dict[labels_dict['resource_detail']] = temp_list
    resource_list.append(temp_main_dict)


    # For Servers
    temp_main_dict = {}
    temp_main_dict[labels_dict['resource_type']] = "server"
    temp_list = []
    for server in Server.objects.filter(cloudinfra=cloudinfra):
        temp_sub_dict = {}

        temp_sub_dict[labels_dict['server_name']] = server.server_name
        temp_sub_dict[labels_dict['image_name']] = server.image
        temp_sub_dict[labels_dict['flavor_name']] = server.flavor
        
        if server.network.network_name == "Public Network":
            temp_sub_dict[labels_dict['network_name']] = 'public'
        else:
            temp_sub_dict[labels_dict['network_name']] = server.network.network_name
        
        if server.network.router != None and server.network.router.router_name == "Public Network Router":
            print("IN FLOAT CONDITION")
            temp_sub_dict[labels_dict['floating_ip']] = server.floating_ip
        else:
            temp_sub_dict[labels_dict['floating_ip']] = False

        temp_sub_dict[labels_dict['server_status']] = server.server_status


        if bool(temp_sub_dict):
            temp_list.append(temp_sub_dict)
    temp_main_dict[labels_dict['resource_detail']] = temp_list
    resource_list.append(temp_main_dict)

    print(resource_list)
    exception_list = big_bang(resource_list)

    context = {
        'exception_list': exception_list,
        'minutes_to_live': cloudinfra.minutes_to_live
    }

    interval = cloudinfra.minutes_to_live * 60
    destruction_time = Timer(interval=interval, function=big_crunch)
    destruction_time.start()

    return render(request, 'teacher/partials/build_infra.html', context)
import 'package:flutter/material.dart';
import 'package:http/http.dart'as http;
import 'dart:convert';

void main()  {
    runApp(BusinessApp());
}
class BusinessApp extends 
statelesswidget{
    @override
    widget build(BusinessApp(
        title:'Business platform',
        theme:
        themeData.dart(),
        hom:Loginscreen(),
    ),
    )
}
class Loginscreen extends
statefulwidget{
    @override
    _loginscreenstate
    createstate()=>
    _loginscreenstate();
}
class _loginscreenstate
extends state<Loginscreen>{
    final username=
    TextEditingController();
    final password=
    TextEditingController()
    void login() async{
        var res = await
        http.post(
            Uri.parse("http://<YOUR_SERVER_IP>:8000/login"),
            body:
            json.encode({"username":
            username.text,"password":
            password.text}),
            headers:
            {"content-type":"application/json"}
        );
        if (res.statuscode == 200){
            Navigator.push(context,MaterialPageRoute(builder:(_)=>Dashboard()));
        }
    }
    @override
    widget build(Buildcontex
    context){
        return scanffold(
            appBar:AppBar(title:Text("Login")),
            body:column(
                children:[
                    TextField(controller:
                    username,decoration:
                    InputDecoration(hintText:
                    "username")),
                    TextField(controller:
                    password,decoration:
                    InputDecoration(hintText:
                    "Password"), obscureText:
                    true),
                    ElevatedButton(onpressed:
                    login,child:Text("Login"))
                ],
            ),
        ),
    }
}
class Dashboard extends
statelesswidget{
    @override
    widget build(Buildcontex
    context) {
        return scanffold(
            appBar:AppBar(title:
            Text("Dashboard")),
            body:Center(child:
            Text("Bienvenue sur le
            Dashboard Mobile!")),
        );
    }
}
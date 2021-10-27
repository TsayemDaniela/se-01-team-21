const http = require('http');
const host = 'http://localhost';
const port = '5000'
const axios = require('axios')
var request = require('request')
const XMLHttpRequest = require('xmlhttprequest').XMLHttpRequest;
var auth_name
var auth_pass
const assert = require('assert')
describe('testing the authentication api', async function(){
    it('an instructor can try to register', async function() {
        let randnum = (Math.floor(Math.random() * 10203040))
        auth_name = 'user_test'+ randnum
        auth_pass = '12345'

        var cnf = {name: auth_name, password: auth_pass}

    //    http.get('http://localhost:5000', res=>{
    //        console.log(res);
    //    })
        let xd = await new Promise((resolve , reject)=>{
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://localhost:5000/auth/signup', true)
        xhr.onload = function(e){
                console.log(xhr.responseText)
                resolve(xhr.status)
            //  assert(xhr.status == 200, 'status is not 200')
        }
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
        xhr.send(JSON.stringify(cnf))
        })
        assert(xd, 200, 'status is not 200')
       
    });
    it('an instructor can log in', async function() {
        let randnum = (Math.floor(Math.random() * 10203040));
        var cnf = {name: auth_name, password: auth_pass}
        let res = await new Promise((resolve , reject)=>{
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://localhost:5000/auth/register', true)
        xhr.onload = function(e){
            console.log(xhr.responseText);
            resolve(xhr.status);
        //    assert(xhr.status == 201, 'status is not 200')
        }
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
        xhr.send(JSON.stringify(cnf))
        console.log(JSON.stringify(cnf))
        })
        assert(res == 200, "result is not 200")   
    });
    it('a non-authenticated instructor cannot register a game', async function() {
        var cnf = {name: auth_name, password: auth_pass}
        let res = await new Promise((resolve , reject)=>{
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://localhost:5000/instructor/create_game', true)
        xhr.onload = function(e){
            console.log(xhr.responseText);
            resolve(xhr.status);
        //    assert(xhr.status == 201, 'status is not 200')
        }
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
        xhr.send(JSON.stringify(cnf))
        console.log(JSON.stringify(cnf))
        })
        assert(res >= 400, "the result should be invalid!")   
    });

       
    


        

})


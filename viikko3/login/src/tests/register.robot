*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  Pekka
    Set Password  Pekka123
    Set Password Confirmation  Pekka123
    Click Button  Register
    Title Should Be  Welcome to Ohtu Application!


Register With Too Short Username And Valid Password
    Set Username  P
    Set Password  Pekka123
    Set Password Confirmation  Pekka123
    Click Button  Register
    Page Should Contain  Username or password too short

Register With Valid Username And Too Short Password
    Set Username  Pekka
    Set Password  P
    Set Password Confirmation  P
    Click Button  Register
    Page Should Contain  Username or password too short

Register With Valid Username And Invalid Password
# salasana ei sisällä halutunlaisia merkkejä
    Set Username  Pekka
    Set Password  Pekka
    Set Password Confirmation  Pekka
    Click Button  Register
    Page Should Contain  Invalid password

Register With Nonmatching Password And Password Confirmation
    Set Username  Pekka
    Set Password  Pekka123
    Set Password Confirmation  Pekka678
    Click Button  Register
    Page Should Contain  Passwords do not match

Register With Username That Is Already In Use
    Set Username  Pekka
    Set Password  Pekka123
    Set Password Confirmation  Pekka123
    Click Button  Register
    Page Should Contain  Welcome to Ohtu Application!
    Go To Register Page
    Set Username  Pekka
    Set Password  Pekka123
    Set Password Confirmation  Pekka123
    Click Button  Register
    Page Should Contain  User with username Pekka already exists

*** Keywords ***
Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page

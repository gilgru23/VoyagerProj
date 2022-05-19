
const prefix = "android:id/voyagerconsumer/";
const homeScreenPrefix = prefix + "home/";
const regScreenPrefix = prefix + "register/";
const loginScreenPrefix = prefix + "login/";
const personalInfoFormScreenPrefix = regScreenPrefix + "info/";
export class ResourceIds{
    //home screen
    static home_register_btn = homeScreenPrefix + "register";
    static home_login_btn = homeScreenPrefix + "login";
    
    //register screen
    static reg_firstName_et = regScreenPrefix + "firstName";
    static reg_lastName_et = regScreenPrefix + "lastName";
    static reg_email_et = regScreenPrefix + "email";
    static reg_password_et = regScreenPrefix + "password";
    static reg_dob_btn = regScreenPrefix + "dobButton";
    static reg_calendarSubmit_btn = "android:id/button1";
    static reg_submit_btn = regScreenPrefix + "submit";

    //personal info
    static regPersonalInfo_submit_btn = personalInfoFormScreenPrefix + "submit";


    //login screen
    static login_email_et = loginScreenPrefix + "email";
    static login_password_et = loginScreenPrefix + "password";
    static login_profileType_dropdown = loginScreenPrefix + "profileType";
    static login_submit = loginScreenPrefix + "submit";

//edittext
}
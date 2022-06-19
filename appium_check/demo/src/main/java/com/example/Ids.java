package com.example;

public class Ids {
    static final String prefix = "android:id/voyagerconsumer/";
    static final String homeScreenPrefix = prefix + "home/";
    static final String regScreenPrefix = prefix + "register/";
    static final String loginScreenPrefix = prefix + "login/";
    static final String personalInfoFormScreenPrefix = regScreenPrefix + "info/";

    
    //home screen
    public static final String home_register_btn = homeScreenPrefix + "register";
    public static final String home_login_btn = homeScreenPrefix + "login";
    
    //register screen
    public static final String reg_firstName_et = regScreenPrefix + "firstName";
    public static final String reg_lastName_et = regScreenPrefix + "lastName";
    public static final String reg_email_et = regScreenPrefix + "email";
    public static final String reg_password_et = regScreenPrefix + "password";
    public static final String reg_dob_btn = regScreenPrefix + "dobButton";
    public static final String reg_calendarSubmit_btn = "android:id/button1";
    public static final String reg_submit_btn = regScreenPrefix + "submit";

    //register personal info screen
    public static final String regPersonalInfo_residence_et = personalInfoFormScreenPrefix + "residence";
    public static final String regPersonalInfo_submit_btn = personalInfoFormScreenPrefix + "submit";
    
    //login screen
    public static final String login_email_et = loginScreenPrefix + "email";
    public static final String login_password_et = loginScreenPrefix + "password";
    public static final String login_profileType_dropdown = loginScreenPrefix + "profileType";
    public static final String login_submit = loginScreenPrefix + "submit";
}

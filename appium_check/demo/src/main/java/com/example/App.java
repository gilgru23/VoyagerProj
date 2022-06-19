// package demo.src.main.java.com.example;
//#region imports
package com.example;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Random;
import java.util.Scanner;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
// import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.DesiredCapabilities;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.AppiumBy.ByAccessibilityId;
// import io.appium.java_client.MobileElement;
import io.appium.java_client.android.AndroidDriver;
import java.util.Random;
//#endregion imports

public class App 
{
    // WebDriver w;
    // static AppiumDriver driver;
    static AndroidDriver driver;
    static String EMAIL = "";
    static final String PASSWORD = "fcc32UHJ@#4kj";
    static final int WAIT_TIME = 3000;

    public static void main( String[] args )
    {
        EMAIL = "mrflin" + new Random().nextInt(99999999) + "@yahoo.com";
        System.out.println( "Hello Mothafuckin' World!" );
        try {
            openVoyager();
        }catch(Exception e){
            printError(e);
        }
    }

    static void openVoyager() throws MalformedURLException, InterruptedException{
        //init
        DesiredCapabilities cap = getCapabilities();
        URL url = new URL("http://127.0.0.1:4723/wd/hub");
        driver = new AndroidDriver(url, cap);
        Thread.sleep(3000);
        // printToFile("homepage.xml", driver.getPageSource());

        //registration
        clickElementWithId(Ids.home_register_btn);
        Thread.sleep(WAIT_TIME);
        fillEditText(Ids.reg_firstName_et, "Fred");
        fillEditText(Ids.reg_lastName_et, "Flintstone");
        fillEditText(Ids.reg_email_et, EMAIL);
        fillEditText(Ids.reg_password_et, PASSWORD);
        clickElementWithId(Ids.reg_submit_btn);
        Thread.sleep(WAIT_TIME);

        //create consumer profile
        // printToFile("infopage.xml", driver.getPageSource());
        fillEditText(Ids.regPersonalInfo_residence_et, "48237");
        clickElementWithId(Ids.regPersonalInfo_submit_btn);

    }

    static void clickElementWithId(String id){
        WebElement button = driver.findElement(By.id(id));
        button.click();
    }
    
    static void fillEditText(String elementId, String text){
        WebElement editText = driver.findElement(By.id(elementId));
        editText.sendKeys(text);

    }


    static void printToFile(String fileName, String s){
        try {
            File myObj = new File(fileName);
            if (myObj.createNewFile()) {
            } else {
            }
            FileWriter myWriter = new FileWriter(fileName );
            myWriter.write(s);
            myWriter.close();
          } catch (IOException e) {
            e.printStackTrace();
          }
    }


    static DesiredCapabilities getCapabilities(){
        DesiredCapabilities cap = new DesiredCapabilities();
        //or cmd 'adb shell', cmd "dumpsys window windows | grep -E 'mCurrentFocus'"
        // cap.setCapability("appPackage", "com.sec.android.app.popupcalculator");
        // cap.setCapability("appActivity", "com.sec.android.app.popupcalculator.Calculator");
        cap.setCapability("deviceName", "Galaxy A70");
        cap.setCapability("udid", "R58M73C8EFK");//output from 'adb devices' command in cmd
        cap.setCapability("platformName", "Android");
        cap.setCapability("platformVersion", "9");//android version in phone settings
        cap.setCapability("appPackage", "com.awesomeproject");
        cap.setCapability("appActivity", "com.awesomeproject.MainActivity");
        cap.setCapability("automationName", "uiautomator2");//“automationName”: “uiautomator2”

        return cap;
    }
    static DesiredCapabilities getCapabilitiesGalaxyA5(){
        DesiredCapabilities cap = new DesiredCapabilities();
        cap.setCapability("deviceName", "Galaxy A5 (2017)");
        cap.setCapability("udid", "520041dbecd964bf");//output from 'adb devices' command in cmd
        cap.setCapability("platformName", "Android");
        cap.setCapability("platformVersion", "7.0");//android version in phone settings
        cap.setCapability("appPackage", "com.sec.android.app.popupcalculator");
        cap.setCapability("appActivity", "com.sec.android.app.popupcalculator.Calculator");
        return cap;
    }
    static void printError(Exception e){
        // System.out.println("cause:\n");
        // System.out.println(e.getCause());
        System.out.println("ERROR message:\n");
        System.out.println(e.getMessage());
        printToFile("errormsg.txt", e.getMessage());
        // System.out.println("stack trace:\n");
        // e.printStackTrace();
    }
    
    static String getUniqueEmail(){
        return "mrflin" + getUniqueNumber() + "@gmail.com";
    }

    static String getUniqueNumber(){
        String fileName = "emailnum.txt";
        try {
            File myObj = new File(fileName);
            FileWriter myWriter = new FileWriter(fileName );
            Scanner myReader = new Scanner(new FileInputStream(myObj));
            String output;
            if (!myReader.hasNext()) {
                myWriter.write("1011");
                myWriter.close();
                output = "1010";
            } else {
                output = myReader.nextLine();
                int a = Integer.parseInt(output);
                output = "" + a;
                a++;
                myWriter.write("" + a);
                myWriter.close();
            }
            System.out.println("\n\n\nnumber is " + output + "\n\n\n");
            return output;
          } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
            return "";
          }        
    }
}

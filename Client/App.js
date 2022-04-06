import { StatusBar } from "expo-status-bar";
import React, { useState } from "react";
import RNBluetoothClassic, {
  BluetoothDevice
} from 'react-native-bluetooth-classic';import {
  StyleSheet,
  Text,
  View,
  Image,
  TextInput,
  Button,
  TouchableOpacity,
  PermissionsAndroid
} from "react-native";
 
export default function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [bondedDevices, setBondedDevices] = useState([])
  
  const requestAccessFineLocationPermission = async () => {
    const granted = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.BLUETOOTH_CONNECT,
      {
        title: 'Access fine location required for discovery',
        message:
          'In order to perform discovery, you must enable/allow ' +
          'fine location access.',
        buttonNeutral: 'Ask Me Later',
        buttonNegative: 'Cancel',
        buttonPositive: 'OK',
      }
    );
    return granted === PermissionsAndroid.RESULTS.GRANTED;
  };

  const bluetoothScan = async () => {
    await requestAccessFineLocationPermission()
    try {
      const devices = await RNBluetoothClassic.getBondedDevices();
      setBondedDevices(devices)
      // this.setState({ available });
    } catch (err) {
      console.log(err)
    }
  }
 
  return (
    <View style={styles.container}>
      {/* <Image style={styles.image} source={require("./assets/voyagerLogo.png")} /> */}
      {/* <Image style={styles.dispenserImg} source={require("./assets/dispenser.png")} /> */}
      <Button title='Add new goals' onPress={() => bluetoothScan("")}/>
      <Text>Bonded Devices List:</Text>
      {
        bondedDevices.map(device => <Text>{device["_nativeDevice"]["name"]}</Text>)
      }
      

      

{/*  
      <StatusBar style="auto" />
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Email."
          placeholderTextColor="#003f5c"
          onChangeText={(email) => setEmail(email)}
        />
      </View>
 
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Password."
          placeholderTextColor="#003f5c"
          secureTextEntry={true}
          onChangeText={(password) => setPassword(password)}
        />
      </View>
 
      <TouchableOpacity>
        <Text style={styles.forgot_button}>Forgot Password?</Text>
      </TouchableOpacity>
       */}
      <View style={styles.buttonLayout}>
        <TouchableOpacity style={styles.loginBtn}>
            <Text style={styles.loginText}>LOGIN</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.loginBtn}>
            <Text style={styles.loginText}>Register</Text>
        </TouchableOpacity>
      </View>
    </View>
    
  );
}
 
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
 
  image: {
  },

  dispenserImg: {
      height: "50%",
      width: "50%"
  },
 
  inputView: {
    backgroundColor: "#eee",
    borderRadius: 30,
    width: "70%",
    height: 45,
    marginBottom: 20,
 
    alignItems: "center",
  },
 
  TextInput: {
    height: 50,
    flex: 1,
    padding: 10,
    marginLeft: 20,
  },
 
  forgot_button: {
    height: 30,
    marginBottom: 30,
  },
 
  buttonLayout : {
    display: "flex",
    flexDirection: "row"
  }, 
  
  loginBtn: {
    width: "50%",
    borderRadius: 25,
    height: 50,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 40,
    backgroundColor: "#eee",
  },
});
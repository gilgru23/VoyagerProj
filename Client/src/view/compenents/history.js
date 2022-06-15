// components/login.js
import React, { useState, useEffect } from 'react'
import { StyleSheet, FlatList, Image } from 'react-native'
import { Picker } from '@react-native-picker/picker'
import DateTimePicker from '@react-native-community/datetimepicker'
import PushNotification from 'react-native-push-notification'
import { alert } from './utils'
import { responseStatus } from '../../Config/constants'
import {
  Colors,
  BorderRadiuses,
  View,
  ListItem,
  Text
} from 'react-native-ui-lib'

export default function History({ navigation, route }) {
  const [dosingHistory, setDosingHistory] = useState([])

  const keyExtractor = (item) => item.pod_serial_number
  const statusColor = Colors.green30
  useEffect(() => {
    const getHistory = async () => {
      const response = await route.params.controller.getDosingHistory()
      if (response.status === responseStatus.SUCCESS) {
        console.log(response.content)
        const dosingFeedback = await route.params.controller.getFeedback(
          response.content[0].id
        )
        console.log('dosing feeback:', dosingFeedback)
        setDosingHistory(response.content)
      }
    }
    getHistory()
  }, [])

  const renderRow = (row, id) => (
    <View>
      <ListItem
        // @ts-expect-error
        containerStyle={{ marginBottom: 3 }}
        activeBackgroundColor={Colors.grey60}
        activeOpacity={0.3}
        height={77.5}
        onPress={() =>
          navigation.navigate('Dosing Feedback', {
            dosing: row,
            consumer: route.params.consumer
          })
        }
      >
        <ListItem.Part left>
          <Image source={require('./assets/dosing.png')} style={styles.image} />
        </ListItem.Part>
        <ListItem.Part
          middle
          column
          containerStyle={[styles.border, { paddingRight: 17 }]}
        >
          <ListItem.Part containerStyle={{ marginBottom: 3 }}>
            {/* <Text
              style={{ flex: 1, marginRight: 10 }}
              text90
              grey40
              numberOfLines={1}
            >
              {`Pod Type Num: ${row.pod_type_name}`}
            </Text> */}
            <Text
              style={{ flex: 1, marginRight: 10 }}
              text90
              grey40
              numberOfLines={1}
            >
              {`Pod Serial Num: ${row.podSerialNum}`}
            </Text>
          </ListItem.Part>
          <ListItem.Part containerStyle={{ marginBottom: 3 }}>
            {/* <Text
              style={{ flex: 1, marginRight: 10 }}
              text90
              grey40
              numberOfLines={1}
            >
              {`Pod Type Num: ${row.pod_type_name}`}
            </Text> */}
            <Text
              style={{ flex: 1, marginRight: 10 }}
              text90
              grey40
              numberOfLines={1}
            >
              {`Pod Type: ${row.podType}`}
            </Text>
          </ListItem.Part>
          <ListItem.Part containerStyle={{ marginBottom: 3 }}>
            {/* <Text
              style={{ flex: 1, marginRight: 10 }}
              text90
              grey40
              numberOfLines={1}
            >
              {`Amount: ${row.amount}`}
            </Text> */}
            <Text style={{ flex: 1 }} text90 grey40 numberOfLines={1}>
              {`Time of dosing: ${row.time}`}
            </Text>
          </ListItem.Part>
          <ListItem.Part containerStyle={{ marginBottom: 3 }}>
            {/* <Text
              style={{ flex: 1, marginRight: 10 }}
              text90
              grey40
              numberOfLines={1}
            >
              {`Amount: ${row.amount}`}
            </Text> */}
            <Text style={{ flex: 1 }} text90 grey40 numberOfLines={1}>
              {`Amount: ${row.amount}`}
            </Text>
          </ListItem.Part>
        </ListItem.Part>
      </ListItem>
    </View>
  )

  return (
    <>
      <Text style={styles.header}>Dosing history</Text>
      <Text style={styles.subHeader}>Press on dosing item to feedback him</Text>
      <FlatList
        data={dosingHistory}
        renderItem={({ item, index }) => renderRow(item, index)}
        keyExtractor={keyExtractor}
      />
    </>
  )
}
const styles = StyleSheet.create({
  header: {
    fontSize: 30,
    marginBottom: 20,
    textAlign: 'center'
  },
  subHeader: {
    fontSize: 20,
    marginBottom: 40,
    textAlign: 'center'
  },
  image: {
    width: 54,
    height: 70,
    borderRadius: BorderRadiuses.br20,
    marginHorizontal: 14
  },
  border: {
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderColor: Colors.black
  }
})

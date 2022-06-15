// components/login.js
import React, { useState, useEffect } from 'react'
import { StyleSheet, FlatList, Image } from 'react-native'
import { responseStatus } from '../../Config/constants'
import {
  Colors,
  BorderRadiuses,
  View,
  ListItem,
  Text
} from 'react-native-ui-lib'

export default function History({ navigation, route }) {
  const [currPods, setCurrPods] = useState([])

  const keyExtractor = (item) => item.id
  useEffect(() => {
    const getPods = async () => {
      const response = await route.params.controller.getPods()
      if (response.status === responseStatus.SUCCESS) {
        console.log(response.content)
        setCurrPods(response.content)
      }
    }
    getPods()
  }, [])

  const renderRow = (row, id) => (
    <View>
      <ListItem
        containerStyle={{ marginBottom: 3 }}
        activeBackgroundColor={Colors.grey60}
        activeOpacity={0.3}
        height={77.5}
      >
        <ListItem.Part left>
          <Image source={require('./assets/pod.png')} style={styles.image} />
        </ListItem.Part>
        <ListItem.Part
          middle
          column
          containerStyle={[styles.border, { paddingRight: 17 }]}
        >
          <ListItem.Part containerStyle={{ marginBottom: 3 }}>
            <Text
              style={{ flex: 1, marginRight: 10 }}
              text90
              grey40
              numberOfLines={1}
            >
              {`Pod Serial Num: ${row.id}`}
            </Text>
          </ListItem.Part>
          <ListItem.Part containerStyle={{ marginBottom: 3 }}>
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
            <Text style={{ flex: 1 }} text90 grey40 numberOfLines={1}>
              {`Remainder: ${row.remainder}`}
            </Text>
          </ListItem.Part>
        </ListItem.Part>
      </ListItem>
    </View>
  )

  return (
    <>
      <Text style={styles.header}>Current Pods</Text>
      <FlatList
        data={currPods}
        renderItem={({ item, index }) => renderRow(item, index)}
        keyExtractor={keyExtractor}
      />
    </>
  )
}
const styles = StyleSheet.create({
  header: {
    fontSize: 30,
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

import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:intl/intl.dart';

void main() => runApp(MaterialApp(home: MyApp()));

class MyApp extends StatelessWidget {
  var _firestoreRef = Firestore.instance.collection('chats');
  TextEditingController _txtCtrl = TextEditingController();

  sendMessage() {
    _firestoreRef.add({
      "message": _txtCtrl.text,
      "timestamp": DateTime.now().millisecondsSinceEpoch
    });
    _txtCtrl.clear();
  }

  deleteMessage(key) {
    _firestoreRef.document(key).delete();
  }

  updateTimeStamp(key) {
    _firestoreRef
        .document(key)
        .updateData({"timestamp": DateTime.now().millisecondsSinceEpoch});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text("FlutterOwl"),
        ),
        body: Column(mainAxisAlignment: MainAxisAlignment.start, children: <
            Widget>[
          Expanded(
            child:
            StreamBuilder(
              stream: _firestoreRef.snapshots(),
              builder: (context, snapshot) {
                if (!snapshot.hasData)
                  return LinearProgressIndicator();
                else {
                  List item = [];
                  snapshot.data.documents.forEach((document) {
                    // print(document.documentID);
                    // print(document.data);
                    item.add({"key": document.documentID, ...document.data});
                  });

                  return ListView.builder(
                    itemCount: item.length,
                    itemBuilder: (context, index) {
                      return ListTile(
                        title: Text(item[index]['message']),
                        trailing: Text(DateFormat("hh:mm:ss")
                            .format(DateTime.fromMicrosecondsSinceEpoch(
                                item[index]['timestamp'] * 1000))
                            .toString()),
                        onTap: () => updateTimeStamp(item[index]['key']),
                        onLongPress: () => deleteMessage(item[index]['key']),
                      );
                    },
                  );
                }
              },
            ),
          ),
          Container(
              child: Row(children: <Widget>[
            Expanded(child: TextField(controller: _txtCtrl)),
            SizedBox(
                width: 80,
                child: OutlineButton(
                    child: Text("Add"), onPressed: () => sendMessage()))
          ]))
        ]));
  }
}

import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:intl/intl.dart';
import 'package:rflutter_alert/rflutter_alert.dart';
import 'package:url_launcher/url_launcher.dart';



class EGov extends StatelessWidget {
  var _firestoreRef = Firestore.instance.collection('E-gov');
  TextEditingController _txtCtrl = TextEditingController();

  _launchURL(url) async {
    if (await canLaunch(url)) {
      await launch(url);
    } else {
      throw 'Could not launch $url';
    }
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
          title: Text("E-governance"),
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
                        title: Text(item[index]['key'].toString()),

                        onTap: () {
                          return Alert(
                            context: context,
                            title: (item[index]['key'].toString()),
                            desc:"Please vote if you Support the bill or not",
                            buttons: [
                              DialogButton(
                                child: Text("Support"),
                                onPressed: (){},
                              ),
                              DialogButton(
                                child: Text("Disregard"),
                                onPressed: (){},
                              ),
                              DialogButton(
                                child: Text("Learn More"),
                                onPressed:  (){_launchURL(item[index]['BIll_link']);},
                              ),
                            ]


                          ).show();
                        },

                      );
                    },
                  );
                }
              },
            ),
          ),

        ]));
  }
}

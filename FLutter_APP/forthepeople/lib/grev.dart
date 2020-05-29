import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_form_bloc/flutter_form_bloc.dart';
import 'package:form_bloc/form_bloc.dart';
import 'package:forthepeople/sign_in.dart';
import 'package:forthepeople/widgets/form_button.dart';
import 'package:forthepeople/widgets/widgets.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

import 'egov.dart';
import 'login_page.dart';

class LoginFormBloc extends FormBloc<String, String> {
  LoginFormBloc() {
    addFieldBloc(
      fieldBloc: TextFieldBloc(
        name: 'grevience',
        validators: [FieldBlocValidators.requiredTextFieldBloc],
      ),
    );


  }

  @override
  Stream<FormBlocState<String, String>> onSubmitting() async* {
    // Login logic...

    // Get the fields values:
    print(state.fieldBlocFromPath('grevience').asTextFieldBloc.value);
    print(email);
    final databaseReference = Firestore.instance;
    DocumentReference ref = await databaseReference.collection("REPORTS")
        .add({
      'UID': email,
      'report': state.fieldBlocFromPath('grevience').asTextFieldBloc.value
    });
    print(ref.documentID);
    print(email);
    await databaseReference.collection("REPORTS_UNCLASSIFIED")
        .document(ref.documentID)
        .setData({
      'UID': email,
      'report': state.fieldBlocFromPath('grevience').asTextFieldBloc.value
    });


    await databaseReference.collection("Async")
        .document('State')
        .setData({
      'val': '1',
    });



    await Future<void>.delayed(Duration(seconds: 1));
    yield state.toSuccess();
  }
}

class LoginForm extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider<LoginFormBloc>(
      create: (context) => LoginFormBloc(),
      child: Builder(
        builder: (context) {
          return Scaffold(
            appBar: AppBar(title: Text('Greviences')),
            body: FormBlocListener<LoginFormBloc, String, String>(
              onSubmitting: (context, state) => LoadingDialog.show(context) ,
              onSuccess: (context, state) {
                LoadingDialog.hide(context);
                Navigator.of(context).pushReplacementNamed('success');
              },
              onFailure: (context, state) {
                LoadingDialog.hide(context);
                Notifications.showSnackBarWithError(
                    context, state.failureResponse);


              },
              child: BlocBuilder<LoginFormBloc, FormBlocState>(
                builder: (context, state) {
                  return ListView(
                    physics: ClampingScrollPhysics(),
                    children: <Widget>[
                      TextFieldBlocBuilder(
                        textFieldBloc: state.fieldBlocFromPath('grevience'),
                        keyboardType: TextInputType.emailAddress,
                        decoration: InputDecoration(
                          labelText: 'Enter Your Grevience',
                          prefixIcon: Icon(Icons.input),
                        ),
                      ),
                      FormButton(
                        text: 'SUBMIT',
                        onPressed: context.bloc<LoginFormBloc>().submit,
                      ),
                      FormButton(
                        text: 'E-Governance',
                        onPressed: () {
                          Navigator.of(context).pushAndRemoveUntil(MaterialPageRoute(builder: (context) {return EGov();}), ModalRoute.withName('/'));
                        },
                      ),
                      RaisedButton(
                        onPressed: () {
                          signOutGoogle();
                          Navigator.of(context).pushAndRemoveUntil(MaterialPageRoute(builder: (context) {return LoginPage();}), ModalRoute.withName('/'));
                        },
                        color: Colors.deepPurple,
                        child: Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: Text(
                            'Sign Out',
                            style: TextStyle(fontSize: 25, color: Colors.white),
                          ),
                        ),
                        elevation: 5,
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(40)),
                      )
                    ],
                  );
                },
              ),
            ),
          );
        },
      ),
    );
  }
}
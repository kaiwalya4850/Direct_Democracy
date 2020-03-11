import 'package:form_bloc/form_bloc.dart';

class NotAutoValidationFormBloc extends FormBloc<String, String> {
  NotAutoValidationFormBloc() : super(autoValidate: false) {
    addFieldBloc(
      fieldBloc: TextFieldBloc(
        name: 'email',
        validators: [FieldBlocValidators.email],
      ),
    );

    addFieldBloc(
      fieldBloc: TextFieldBloc(
        name: 'password',
        validators: [FieldBlocValidators.requiredTextFieldBloc],
      ),
    );
  }

  @override
  Stream<FormBlocState<String, String>> onSubmitting() async* {
    // Login logic...

    // Get the fields values:
    print(state.fieldBlocFromPath('email').asTextFieldBloc.value);
    print(state.fieldBlocFromPath('password').asTextFieldBloc.value);

    await Future<void>.delayed(Duration(seconds: 2));
    yield state.toSuccess();
  }
}

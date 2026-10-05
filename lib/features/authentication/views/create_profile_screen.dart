import 'package:dartcoder/features/authentication/view_model/app_cubit.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class CreateProfileScreen extends StatefulWidget {
  const CreateProfileScreen({super.key});

  @override
  State<CreateProfileScreen> createState() => _CreateProfileScreenState();
}

class _CreateProfileScreenState extends State<CreateProfileScreen> {
  final _formKey = GlobalKey<FormState>();
  final firstNameController = TextEditingController();
  final lastNameController = TextEditingController();
  String? selectedLevel;

  final List<String> dartLevels = [
    AppString.expert,
    AppString.intermediate,
    AppString.beginner,
  ];

  @override
  void initState() {
    firstNameController.text =
        context.read<AppCubit>().profile?.firstName ?? "";
    lastNameController.text = context.read<AppCubit>().profile?.lastName ?? "";
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<AppCubit, AppState>(builder: (_, state) {
      return Scaffold(
        appBar: AppBar(
          automaticallyImplyLeading: false,
          title: Text(AppString.createProfile),
        ),
        bottomNavigationBar: state is AuthLoading
            ? null
            : SafeArea(
                child: Container(
                  height: 40.h,
                  margin:
                      EdgeInsets.only(bottom: 10.h, left: 20.w, right: 20.w),
                  child: AppButton(
                    onTap: () {
                      if ((_formKey.currentState?.validate() ?? false) &&
                          selectedLevel != null) {
                        context.read<AppCubit>().createProfile(
                              firstName: firstNameController.text,
                              lastName: lastNameController.text,
                              currentLevel: selectedLevel!,
                            );
                      } else if (selectedLevel == null) {
                        AppRouter.showMessage(AppString.pleaseSelectDartLevel);
                      }
                    },
                    text: AppString.save,
                  ),
                ),
              ),
        body: Stack(
          children: [
            Form(
              key: _formKey,
              child: PopScope(
                canPop: false,
                child: SafeArea(
                  child: Padding(
                    padding: EdgeInsets.symmetric(horizontal: 20.w),
                    child: Column(
                      children: [
                        SizedBox(height: 30.h),
                        AppTextFormField(
                          controller: firstNameController,
                          labelText: AppString.firstName,
                          validator: (value) {
                            if (value == null || value.trim().isEmpty) {
                              return AppString.firstNameRequired;
                            }
                            if (value.trim().length < 2) {
                              return AppString.firstNameMinLength;
                            }
                            return null;
                          },
                        ),
                        SizedBox(height: 30.h),
                        AppTextFormField(
                          controller: lastNameController,
                          labelText: AppString.lastName,
                          validator: (value) {
                            if (value == null || value.trim().isEmpty) {
                              return AppString.lastNameRequired;
                            }
                            if (value.trim().length < 2) {
                              return AppString.lastNameMinLength;
                            }
                            return null;
                          },
                        ),
                        SizedBox(height: 30.h),
                        DropdownButtonFormField<String>(
                         initialValue: selectedLevel,
                          hint: Text(AppString.selectDartLevel),
                          decoration: InputDecoration(
                            labelText: AppString.selectDartLevel,
                            labelStyle:
                                Theme.of(context).textTheme.bodySmall?.copyWith(
                                      fontSize: 14.sp,
                                      fontWeight: FontWeight.w400,
                                    ),
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(8.0),
                              borderSide: BorderSide(color: context.colors.outline),
                            ),
                            focusedBorder: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(8.0),
                              borderSide: BorderSide(color: context.colors.primary, width: 2),
                            ),
                          ),
                          items: dartLevels
                              .map((level) => DropdownMenuItem(
                                    value: level,
                                    child: Text(level),
                                  ))
                              .toList(),
                          onChanged: (value) {
                            setState(() {
                              selectedLevel = value;
                            });
                          },
                          validator: (value) => value == null
                              ? AppString.pleaseSelectDartLevel
                              : null,
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
            if (state is AuthLoading) loadingWidget(context)
          ],
        ),
      );
    });
  }
}

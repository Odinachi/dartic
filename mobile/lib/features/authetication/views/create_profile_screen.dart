import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';
import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
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
  final usernameController = TextEditingController();
  String? selectedLevel;

  final List<String> dartLevels = [
    AppString.expert,
    AppString.intermediate,
    AppString.beginner,
  ];

  @override
  void initState() {
    final profile = context.read<AppCubit>().profile;
    firstNameController.text = profile?.firstName ?? "";
    lastNameController.text = profile?.lastName ?? "";
    usernameController.text = profile?.username ?? "";
    selectedLevel = profile?.currentLevel;
    super.initState();
  }

  @override
  void dispose() {
    firstNameController.dispose();
    lastNameController.dispose();
    usernameController.dispose();
    super.dispose();
  }

  void _onSubmit() {
    final isValid = _formKey.currentState?.validate() ?? false;
    if (!isValid) return;

    final isExistingUser =
        context.read<AppCubit>().profile?.currentLevel != null;

    if (!isExistingUser && selectedLevel == null) {
      AppRouter.showMessage(AppString.pleaseSelectDartLevel);
      return;
    }

    final username = usernameController.text.trim();

    if (isExistingUser) {
      context.read<AppCubit>().updateUsername(username);
    } else {
      context.read<AppCubit>().createProfile(
            firstName: firstNameController.text,
            lastName: lastNameController.text,
            username: username,
            currentLevel: selectedLevel!,
          );
    }
  }

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<AppCubit, AppState>(
      listener: (context, state) {
        if (state is AuthError) {
          AppRouter.showMessage(state.message);
        }
      },
      builder: (context, state) {
        final isExistingUser =
            context.read<AppCubit>().profile?.currentLevel != null;
        final isLoading = state is AuthLoading;

      return Scaffold(
        appBar: AppBar(
          automaticallyImplyLeading: false,
          title: Text(
              isExistingUser ? AppString.setUsername : AppString.createProfile),
        ),
        bottomNavigationBar: isLoading
            ? null
            : SafeArea(
                child: Container(
                  height: 40.h,
                  margin:
                      EdgeInsets.only(bottom: 10.h, left: 20.w, right: 20.w),
                  child: AppButton(
                    onTap: _onSubmit,
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
                  child: SingleChildScrollView(
                    child: Padding(
                      padding: EdgeInsets.symmetric(horizontal: 20.w),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          SizedBox(height: 20.h),
                          if (isExistingUser) ...[
                            Text(
                              AppString.setUsernameDesc,
                              style: Theme.of(context)
                                  .textTheme
                                  .bodyMedium
                                  ?.copyWith(
                                    fontSize: 14.sp,
                                    color: AppColors.grey,
                                  ),
                            ),
                            SizedBox(height: 25.h),
                          ],
                          if (!isExistingUser) ...[
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
                            SizedBox(height: 25.h),
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
                            SizedBox(height: 25.h),
                          ],
                          AppTextFormField(
                            controller: usernameController,
                            labelText: AppString.username,
                            prefixText: "@",
                            textCapitalization: TextCapitalization.none,
                            inputFormatters: [
                              FilteringTextInputFormatter.allow(
                                  RegExp(r'[a-zA-Z0-9_]')),
                            ],
                            validator: (value) {
                              if (value == null || value.trim().isEmpty) {
                                return AppString.usernameRequired;
                              }
                              if (value.trim().length < 3) {
                                return AppString.usernameMinLength;
                              }
                              if (!RegExp(r'^[a-zA-Z0-9_]+$')
                                  .hasMatch(value.trim())) {
                                return AppString.usernameInvalid;
                              }
                              return null;
                            },
                          ),
                          if (!isExistingUser) ...[
                            SizedBox(height: 25.h),
                            DropdownButtonFormField<String>(
                              initialValue: selectedLevel,
                              hint: Text(AppString.selectDartLevel),
                              decoration: InputDecoration(
                                labelText: AppString.selectDartLevel,
                                labelStyle: Theme.of(context)
                                    .textTheme
                                    .bodySmall
                                    ?.copyWith(
                                      fontSize: 14.sp,
                                      fontWeight: FontWeight.w400,
                                    ),
                                border: OutlineInputBorder(
                                  borderRadius: BorderRadius.circular(8.0),
                                  borderSide:
                                      BorderSide(color: AppColors.grey),
                                ),
                                focusedBorder: OutlineInputBorder(
                                  borderRadius: BorderRadius.circular(8.0),
                                  borderSide:
                                      BorderSide(color: AppColors.grey),
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
                          SizedBox(height: 30.h),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
            if (isLoading) loadingWidget(context)
          ],
        ),
      );
    });
  }
}

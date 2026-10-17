import 'package:dartcoder/features/authetication/view_model/app_cubit.dart';

import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/assets.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:url_launcher/url_launcher.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: BlocBuilder<AppCubit, AppState>(builder: (context, state) {
      return Stack(
        children: [
          SafeArea(
            child: Padding(
              padding: EdgeInsets.symmetric(horizontal: 20.w),
              child: Column(
                children: [
                  SizedBox(height: 50.h),
                  Center(
                      child: Assets.images.appImg
                          .image(height: 100.h, width: 100.w)),
                  Expanded(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(AppString.welcome,
                            style: Theme.of(context)
                                .textTheme
                                .bodyLarge
                                ?.copyWith(
                                    fontSize: 30, fontWeight: FontWeight.bold)),
                        SizedBox(height: 2.h),
                        Text(AppString.learnAndBuild,
                            style:
                                Theme.of(context).textTheme.bodyLarge?.copyWith(
                                      fontSize: 15,
                                      fontWeight: FontWeight.bold,
                                      color: AppColors.grey,
                                    )),
                        SizedBox(
                          height: 20.h,
                        ),
                        AppButton(
                          onTap: () {
                            context.read<AppCubit>().signIn(false);
                          },
                          textColor: AppColors.white,
                          backgroundColor: AppColors.black,
                          text: AppString.continueWithApple,
                          leftIcon: Assets.svgs.apple.svg(
                              height: 15.h,
                              width: 15.w,
                              color: AppColors.white),
                        ),
                        SizedBox(height: 10.h),
                        AppButton(
                          onTap: () {
                            context.read<AppCubit>().signIn(true);
                          },
                          backgroundColor:
                              AppColors.white.withValues(alpha: 0.1),
                          borderColor: AppColors.grey,
                          text: AppString.continueWithGoogle,
                          leftIcon: Assets.svgs.google.svg(
                            height: 15.h,
                            width: 15.w,
                          ),
                        ),
                        SizedBox(height: 10.h),
                        AppButton(
                          backgroundColor:
                              AppColors.appBlue.withValues(alpha: 0.2),
                          textColor: AppColors.appBlue,
                          onTap: () =>
                              AppRouter.pushAndClear(AppRouter.dashboard),
                          text: AppString.continueAsGuest,
                        ),
                      ],
                    ),
                  ),
                  RichText(
                      textAlign: TextAlign.center,
                      text: TextSpan(
                        text: AppString.byContinuing,
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                              fontSize: 12,
                              color: AppColors.grey,
                            ),
                        children: [
                          TextSpan(
                            recognizer: TapGestureRecognizer()
                              ..onTap = () async {
                                final uri = Uri.parse(
                                    'https://dartcoder-d57cb.web.app/terms.html');
                                if (await canLaunchUrl(uri)) {
                                  await launchUrl(uri,
                                      mode: LaunchMode.externalApplication);
                                }
                              },
                            text: AppString.termsOfService,
                            style: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.copyWith(
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                  color: AppColors.appBlue,
                                ),
                          ),
                          TextSpan(
                            text: AppString.andText,
                            style: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.copyWith(
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                  color: AppColors.grey,
                                ),
                          ),
                          TextSpan(
                            recognizer: TapGestureRecognizer()
                              ..onTap = () async {
                                final uri = Uri.parse(
                                    'https://dartcoder-d57cb.web.app/privacy_policy.html');
                                if (await canLaunchUrl(uri)) {
                                  await launchUrl(uri,
                                      mode: LaunchMode.externalApplication);
                                }
                              },
                            text: AppString.privacyPolicy,
                            style: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.copyWith(
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                  color: AppColors.appBlue,
                                ),
                          ),
                        ],
                      )),
                  SizedBox(height: 20.h),
                ],
              ),
            ),
          ),
          if (state is AuthLoading) loadingWidget(context)
        ],
      );
    }));
  }
}

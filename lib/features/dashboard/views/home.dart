import 'package:dartcoder/shared/app_string.dart';
import 'package:dartcoder/shared/assets.dart';
import 'package:dartcoder/shared/constants.dart';
import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key, this.onCourseTap});
  final VoidCallback? onCourseTap;

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false,
        title: const Text(AppString.dashboard),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: 20.w),
          child: Column(
            children: [
              SizedBox(height: 20.h),
              dashboardCard(onTap: widget.onCourseTap),
              SizedBox(height: 20.h),
              dashboardCard(
                  image: Assets.images.dsa,
                  title: AppString.dsaCourse,
                  desc: AppString.learnDsa,
                  onTap: () {
                    FirebaseAuth.instance.currentUser == null
                        ? AppRouter.pushAndClear(AppRouter.onboarding)
                        : AppRouter.push(AppRouter.dsaList);
                  }),
            ],
          ),
        ),
      ),
    );
  }

  Widget dashboardCard(
      {String title = AppString.dartCourse,
      String desc = AppString.learnTheBasics,
      VoidCallback? onTap,
      AppAssetImage? image}) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(15.r),
        color: Colors.transparent,
        boxShadow: [
          BoxShadow(
            color: context.colors.shadow.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      height: 200.h,
      child: Stack(
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(15.r),
            child: (image ?? Assets.images.dart).image(
              fit: BoxFit.cover,
              width: double.infinity,
              height: 200.h,
            ),
          ),
          Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(15.r),
              gradient: LinearGradient(
                stops: const [0.02, 1, 1],
                colors: [
                  context.colors.surface.withValues(alpha: .5),
                  context.colors.surface,
                  context.colors.surface,
                ],
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
              ),
            ),
          ),
          Padding(
            padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 15.h),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.end,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        fontSize: 25.sp,
                        fontWeight: FontWeight.bold,
                      ),
                ),
                SizedBox(height: 5.h),
                Text(
                  desc,
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        fontSize: 14.sp,
                        fontWeight: FontWeight.w500,
                        color: context.colors.onSurfaceVariant,
                      ),
                ),
                SizedBox(height: 10.h),
                AppButton(
                  text: AppString.start,
                  onTap: onTap,
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}

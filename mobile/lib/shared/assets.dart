import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:lottie/lottie.dart';

class AssetsImageFile {
  const AssetsImageFile();
  //sample
  AppAssetImage get appImg => const AppAssetImage('assets/pngs/dartic.png');
  AppAssetImage get dart => const AppAssetImage('assets/pngs/dart.jpg');
  AppAssetImage get dsa => const AppAssetImage('assets/pngs/dsa.jpg');

  List<AppAssetImage> get values => [appImg];
}

class AppAssetsJson {
  const AppAssetsJson();

  LottieImage get trophy =>
      const LottieImage('assets/jsons/lottie/trophy.json');
  LottieImage get jumpIn =>
      const LottieImage('assets/jsons/lottie/jump_in.json');
}

class AssetsSvgs {
  const AssetsSvgs();

  SvgImage get apple => const SvgImage("assets/svgs/apple.svg");
  SvgImage get google => const SvgImage("assets/svgs/google.svg");
  SvgImage get course => const SvgImage("assets/svgs/course.svg");
  SvgImage get home => const SvgImage("assets/svgs/home.svg");
  SvgImage get editor => const SvgImage("assets/svgs/editor.svg");
  SvgImage get person => const SvgImage("assets/svgs/person.svg");
  SvgImage get volumeUp => const SvgImage('assets/svgs/volume_up.svg');
}

class Assets {
  Assets._();

  static const AssetsImageFile images = AssetsImageFile();
  static const AppAssetsJson json = AppAssetsJson();
  static const AssetsSvgs svgs = AssetsSvgs();
}

class AppAssetImage {
  const AppAssetImage(this._assetName);

  final String _assetName;

  Image image({
    Key? key,
    AssetBundle? bundle,
    ImageFrameBuilder? frameBuilder,
    ImageErrorWidgetBuilder? errorBuilder,
    String? semanticLabel,
    bool excludeFromSemantics = false,
    double? scale,
    double? width,
    double? height,
    Color? color,
    Animation<double>? opacity,
    BlendMode? colorBlendMode,
    BoxFit? fit,
    AlignmentGeometry alignment = Alignment.center,
    ImageRepeat repeat = ImageRepeat.noRepeat,
    Rect? centerSlice,
    bool matchTextDirection = false,
    bool gaplessPlayback = false,
    bool isAntiAlias = false,
    String? package,
    FilterQuality filterQuality = FilterQuality.low,
    int? cacheWidth,
    int? cacheHeight,
  }) {
    return Image.asset(
      _assetName,
      key: key,
      bundle: bundle,
      frameBuilder: frameBuilder,
      errorBuilder: errorBuilder,
      semanticLabel: semanticLabel,
      excludeFromSemantics: excludeFromSemantics,
      scale: scale,
      width: width,
      height: height,
      color: color,
      opacity: opacity,
      colorBlendMode: colorBlendMode,
      fit: fit,
      alignment: alignment,
      repeat: repeat,
      centerSlice: centerSlice,
      matchTextDirection: matchTextDirection,
      gaplessPlayback: gaplessPlayback,
      isAntiAlias: isAntiAlias,
      package: package,
      filterQuality: filterQuality,
      cacheWidth: cacheWidth,
      cacheHeight: cacheHeight,
    );
  }

  AppAssetImage provider() => AppAssetImage(_assetName);

  String get path => _assetName;

  String get keyName => _assetName;
}

class SvgImage {
  const SvgImage(this._assetName);

  final String _assetName;

  SvgPicture svg(
      {Key? key,
      double? width,
      double? height,
      BoxFit fit = BoxFit.contain,
      Color? color}) {
    return SvgPicture.asset(_assetName,
        key: key,
        width: width?.w,
        height: height?.h,
        fit: fit,
        colorFilter:
            color != null ? ColorFilter.mode(color, BlendMode.srcIn) : null);
  }

  String get path => _assetName;

  String get keyName => _assetName;
}

class LottieImage {
  const LottieImage(this._assetName);

  final String _assetName;

  LottieBuilder lottie({
    Animation<double>? controller,
    bool? animate,
    FrameRate? frameRate,
    bool? repeat,
    bool? reverse,
    LottieDelegates? delegates,
    LottieOptions? options,
    void Function(LottieComposition)? onLoaded,
    LottieImageProviderFactory? imageProviderFactory,
    Key? key,
    AssetBundle? bundle,
    Widget Function(BuildContext, Widget, LottieComposition?)? frameBuilder,
    ImageErrorWidgetBuilder? errorBuilder,
    double? width,
    double? height,
    BoxFit? fit,
    String? package,
    bool? addRepaintBoundary,
    void Function(String)? onWarning,
  }) {
    return Lottie.asset(
      _assetName,
      controller: controller,
      animate: animate,
      frameRate: frameRate,
      repeat: repeat,
      reverse: reverse,
      delegates: delegates,
      options: options,
      onLoaded: onLoaded,
      imageProviderFactory: imageProviderFactory,
      key: key,
      bundle: bundle,
      frameBuilder: frameBuilder,
      errorBuilder: errorBuilder,
      width: width,
      height: height,
      fit: fit,
      package: package,
      addRepaintBoundary: addRepaintBoundary,
      onWarning: onWarning,
    );
  }

  String get path => _assetName;

  String get keyName => _assetName;
}

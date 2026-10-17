import 'package:dartcoder/shared/navigation/router.dart';
import 'package:dartcoder/shared/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:shimmer_animation/shimmer_animation.dart';
import 'package:youtube_player_flutter/youtube_player_flutter.dart';

class CustomVideoPlayer extends StatefulWidget {
  final String videoUrl;

  const CustomVideoPlayer({super.key, required this.videoUrl});

  @override
  State<CustomVideoPlayer> createState() => _CustomVideoPlayerState();
}

class _CustomVideoPlayerState extends State<CustomVideoPlayer> {
  late YoutubePlayerController _controller;
  bool _isPlayerReady = false;
  String? _videoId;

  @override
  void initState() {
    super.initState();
    _initializeYouTubePlayer();
  }

  void _initializeYouTubePlayer() {
    try {
      // Extract video ID from YouTube URL
      _videoId = YoutubePlayer.convertUrlToId(widget.videoUrl);

      if (_videoId == null) {
        AppRouter.showMessage('Invalid YouTube URL');
        return;
      }

      _controller = YoutubePlayerController(
        initialVideoId: _videoId!,
        flags: const YoutubePlayerFlags(
          autoPlay: false,
          mute: false,
          enableCaption: true,
          captionLanguage: 'en',
          showLiveFullscreenButton: true,
        ),
      );

      _controller.addListener(() {
        if (_controller.value.isReady && !_isPlayerReady) {
          setState(() {
            _isPlayerReady = true;
          });
        }
      });
    } catch (e) {
      AppRouter.showMessage(e.toString());
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final videoWidth = screenWidth * 0.9;
    final videoHeight = videoWidth / 1.7777777777777777;

    return SizedBox(
      width: videoWidth,
      height: videoHeight,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(20),
        child: _videoId == null
            ? _buildErrorWidget(videoWidth, videoHeight)
            : AnimatedCrossFade(
                crossFadeState: _isPlayerReady
                    ? CrossFadeState.showSecond
                    : CrossFadeState.showFirst,
                duration: const Duration(milliseconds: 500),
                firstChild: _buildLoadingWidget(videoWidth, videoHeight),
                secondChild: _buildYouTubePlayer(videoWidth, videoHeight),
              ),
      ),
    );
  }

  Widget _buildLoadingWidget(double videoWidth, double videoHeight) {
    return Shimmer(
      duration: const Duration(seconds: 2),
      interval: const Duration(seconds: 0),
      color: Colors.white,
      colorOpacity: 0.5,
      enabled: true,
      direction: const ShimmerDirection.fromLTRB(),
      child: Container(
        width: videoWidth,
        height: videoHeight,
        decoration: BoxDecoration(
          color: AppColors.appBlue.withValues(alpha: .3),
          borderRadius: BorderRadius.circular(20),
        ),
        child: const Center(
          child: Icon(
            Icons.play_circle_outline,
            size: 60,
            color: Colors.white54,
          ),
        ),
      ),
    );
  }

  Widget _buildErrorWidget(double videoWidth, double videoHeight) {
    return Container(
      width: videoWidth,
      height: videoHeight,
      decoration: BoxDecoration(
        color: AppColors.grey.withValues(alpha: 0.3),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.error_outline,
              size: 60,
              color: Colors.red,
            ),
            SizedBox(height: 16.h),
            Text(
              'Unable to load video',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: Colors.red,
                    fontWeight: FontWeight.bold,
                  ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildYouTubePlayer(double videoWidth, double videoHeight) {
    return Container(
      width: videoWidth,
      height: videoHeight,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(20),
      ),
      child: YoutubePlayerBuilder(
        onExitFullScreen: () {
          // Handle exit from fullscreen
          setState(() {});
        },
        player: YoutubePlayer(
          controller: _controller,
          showVideoProgressIndicator: true,
          progressIndicatorColor: AppColors.appBlue,
          progressColors: ProgressBarColors(
            playedColor: AppColors.appBlue,
            handleColor: Colors.white,
            bufferedColor: AppColors.grey.withValues(alpha: 0.5),
            backgroundColor: AppColors.grey.withValues(alpha: 0.3),
          ),
          onReady: () {
            setState(() {
              _isPlayerReady = true;
            });
          },
          onEnded: (data) {
            // Handle video end
          },
        ),
        builder: (context, player) {
          return ClipRRect(
            borderRadius: BorderRadius.circular(20),
            child: player,
          );
        },
      ),
    );
  }
}

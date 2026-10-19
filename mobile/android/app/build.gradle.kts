import java.io.FileInputStream
import java.util.Properties



plugins {
    id("com.android.application")
    // START: FlutterFire Configuration
    id("com.google.gms.google-services")
    id("com.google.firebase.crashlytics")
    // END: FlutterFire Configuration
    id("kotlin-android")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

android {
    namespace = "com.odibillz.dartcoder"
    compileSdk = 36
    ndkVersion = "27.0.12077973"

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
        isCoreLibraryDesugaringEnabled = true
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_11.toString()
    }

    defaultConfig {
        // TODO: Specify your own unique Application ID (https://developer.android.com/studio/build/application-id.html).
        applicationId = "com.odibillz.dartcoder"
        // You can update the following values to match your application needs.
        // For more information, see: https://flutter.dev/to/review-gradle-config.
        minSdk = 24
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    
     signingConfigs {
        create("release") {
            if (System.getenv("CM_KEYSTORE_PATH") != null) {
                storeFile = file(System.getenv("CM_KEYSTORE_PATH"))
                keyAlias = System.getenv("CM_KEY_ALIAS")
                keyPassword = System.getenv("CM_KEY_PASSWORD")
                storePassword = System.getenv("CM_KEYSTORE_PASSWORD")
            } else if (keystorePropertiesFile.exists()) {
                keyAlias = keystoreProperties["keyAlias"] as String
                keyPassword = keystoreProperties["keyPassword"] as String
                storeFile = keystoreProperties["storeFile"]?.let { path -> file(path) }
                storePassword = keystoreProperties["storePassword"] as String
            }
        }
    }

    // Fail release builds with a clear message instead of an NPE in
    // signReleaseBundle when no upload key is configured.
    gradle.taskGraph.whenReady {
        val wantsRelease = allTasks.any { it.name.contains("Release") && it.project == project }
        val release = signingConfigs.getByName("release")
        if (wantsRelease && (release.storeFile == null || !release.storeFile!!.exists())) {
            throw GradleException(
                "Release signing isn't configured: add android/key.properties " +
                    "(storeFile, storePassword, keyAlias, keyPassword) or set CM_KEYSTORE_PATH " +
                    "and related env vars. storeFile is resolved relative to android/app/."
            )
        }
    }
     buildTypes {
        getByName("release") {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android.txt"))
        }
        getByName("debug") {
            signingConfig = signingConfigs.getByName("debug")
        }
    }
}

flutter {
    source = "../.."
}

dependencies {
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")
}
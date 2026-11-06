plugins {
  alias(libs.plugins.android.application)
}

android {
  namespace = "com.drmrbot.fightkro"
  compileSdk = 34

  defaultConfig {
    applicationId = "com.drmrbot.fightkro"
    minSdk = 24
    targetSdk = 34
    versionCode = 1
    versionName = "1.0"
  }

  signingConfigs {
    create("release") {
      storeFile = file("release.jks")
      storePassword = "fightkro123"
      keyAlias = "fightkro"
      keyPassword = "fightkro123"
    }
  }

  buildTypes {
    release {
      isMinifyEnabled = false
      signingConfig = signingConfigs.getByName("release")
    }
    debug {
      signingConfig = signingConfigs.getByName("release")
    }
  }

  compileOptions {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
  }

  androidResources {
    noCompress += listOf("glb", "gltf", "mp3", "mp4", "wasm", "webp", "woff2", "woff")
  }
}

dependencies {
}

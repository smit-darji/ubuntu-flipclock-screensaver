#!/usr/bin/env bash
set -e

# Define directories
PROJECT_DIR="$(pwd)"
SDK_DIR="${PROJECT_DIR}/sdk"
JDK_DIR="${SDK_DIR}/jdk"
CMDLINE_TOOLS_DIR="${SDK_DIR}/cmdline-tools"

echo "=== Creating Directories ==="
mkdir -p "${SDK_DIR}"
mkdir -p "${JDK_DIR}"
mkdir -p "${CMDLINE_TOOLS_DIR}"

# 1. Download and Extract OpenJDK 17
echo "=== Downloading OpenJDK 17 ==="
JDK_URL="https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8.1%2B1/OpenJDK17U-jdk_x64_linux_hotspot_17.0.8.1_1.tar.gz"
if [ ! -f "${SDK_DIR}/jdk.tar.gz" ]; then
    wget -q --show-progress -O "${SDK_DIR}/jdk.tar.gz" "${JDK_URL}"
fi

echo "=== Extracting OpenJDK 17 ==="
tar -xzf "${SDK_DIR}/jdk.tar.gz" -C "${JDK_DIR}" --strip-components=1
rm -f "${SDK_DIR}/jdk.tar.gz"

# Set JDK environment variables for this script
export JAVA_HOME="${JDK_DIR}"
export PATH="${JAVA_HOME}/bin:${PATH}"

echo "Java version installed:"
java -version

# 2. Download and Extract Android Command Line Tools
echo "=== Downloading Android Cmdline Tools ==="
CMDLINE_URL="https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"
if [ ! -f "${SDK_DIR}/cmdline.zip" ]; then
    wget -q --show-progress -O "${SDK_DIR}/cmdline.zip" "${CMDLINE_URL}"
fi

echo "=== Extracting Android Cmdline Tools ==="
unzip -q "${SDK_DIR}/cmdline.zip" -d "${CMDLINE_TOOLS_DIR}"
mv "${CMDLINE_TOOLS_DIR}/cmdline-tools" "${CMDLINE_TOOLS_DIR}/latest"
rm -f "${SDK_DIR}/cmdline.zip"

# 3. Create local.properties
echo "=== Writing local.properties ==="
echo "sdk.dir=${SDK_DIR}" > "${PROJECT_DIR}/local.properties"
cat "${PROJECT_DIR}/local.properties"

# 4. Accept Android SDK licenses
echo "=== Accepting Licenses ==="
yes | "${CMDLINE_TOOLS_DIR}/latest/bin/sdkmanager" --sdk_root="${SDK_DIR}" --licenses

# 5. Install SDK components
echo "=== Installing SDK Components ==="
"${CMDLINE_TOOLS_DIR}/latest/bin/sdkmanager" --sdk_root="${SDK_DIR}" \
    "platform-tools" \
    "platforms;android-34" \
    "build-tools;34.0.0"

echo "=== SDK setup complete ==="

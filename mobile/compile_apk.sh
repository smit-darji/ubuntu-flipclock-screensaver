#!/usr/bin/env bash
set -e

# Directories
PROJECT_DIR="$(pwd)"
SDK_DIR="${PROJECT_DIR}/sdk"
JDK_DIR="${SDK_DIR}/jdk"

# Set environment
export JAVA_HOME="${JDK_DIR}"
export PATH="${JAVA_HOME}/bin:${PATH}"

# Download Gradle if not already there
GRADLE_VER="8.2.1"
GRADLE_ZIP="${SDK_DIR}/gradle-${GRADLE_VER}-bin.zip"
GRADLE_HOME="${SDK_DIR}/gradle-${GRADLE_VER}"

if [ ! -d "${GRADLE_HOME}" ]; then
    echo "=== Downloading Gradle ${GRADLE_VER} ==="
    curl -L -o "${GRADLE_ZIP}" "https://services.gradle.org/distributions/gradle-${GRADLE_VER}-bin.zip"
    echo "=== Extracting Gradle ==="
    unzip -q "${GRADLE_ZIP}" -d "${SDK_DIR}"
    rm -f "${GRADLE_ZIP}"
fi

# Run Gradle Build
echo "=== Building Android APK ==="
"${GRADLE_HOME}/bin/gradle" assembleDebug

echo "=== Build Complete ==="

#!/usr/bin/env python3
"""
🚀 QUICK START EXAMPLE - Viral Video Generator

This script demonstrates basic usage of the system.
"""

from main_integrated import ViralVideoGenerator, Config
import os

def example_1_basic():
    """Example 1: Basic usage with default settings"""
    print("\n" + "="*60)
    print("EXAMPLE 1: BASIC USAGE".center(60))
    print("="*60 + "\n")
    
    # Create default config
    config = Config()
    
    # Create generator
    generator = ViralVideoGenerator(config)
    
    # Run
    generator.run()


def example_2_custom_settings():
    """Example 2: Custom configuration"""
    print("\n" + "="*60)
    print("EXAMPLE 2: CUSTOM SETTINGS".center(60))
    print("="*60 + "\n")
    
    # Create custom config
    config = Config()
    config.INPUT_VIDEO = "myvideo.mp4"       # Your video
    config.OUTPUT_VIDEO = "result_hd.mp4"    # Output name
    config.WHISPER_MODEL = "medium"          # Smaller/faster model
    config.PRESET = "fast"                   # Faster rendering
    config.DEVICE = "cuda"                   # Use GPU if available
    config.CONTENT_ANALYSIS_NUM = 5          # Find 5 moments instead of 3
    
    # Create and run
    generator = ViralVideoGenerator(config)
    generator.run()


def example_3_analysis_only():
    """Example 3: Analysis without rendering"""
    print("\n" + "="*60)
    print("EXAMPLE 3: ANALYSIS ONLY (NO RENDERING)".center(60))
    print("="*60 + "\n")
    
    config = Config()
    config.RENDER_OUTPUT = False  # Skip rendering step
    config.ENABLE_VISION = True   # Still analyze video
    
    generator = ViralVideoGenerator(config)
    generator.run()
    
    # Result: analysis_report.json only (no video output)


def example_4_no_vision():
    """Example 4: Without Vision component (faster)"""
    print("\n" + "="*60)
    print("EXAMPLE 4: FAST MODE (NO VISION)".center(60))
    print("="*60 + "\n")
    
    config = Config()
    config.ENABLE_VISION = False       # Disable face detection
    config.ENABLE_9_16_FORMAT = False  # Disable vertical format
    config.PRESET = "ultrafast"        # Fastest render preset
    config.WHISPER_MODEL = "base"      # Smaller model
    
    generator = ViralVideoGenerator(config)
    generator.run()


def example_5_cpu_mode():
    """Example 5: CPU-only mode (no GPU needed)"""
    print("\n" + "="*60)
    print("EXAMPLE 5: CPU MODE (NO GPU)".center(60))
    print("="*60 + "\n")
    
    config = Config()
    config.DEVICE = "cpu"              # Use CPU
    config.WHISPER_MODEL = "base"      # Smaller model for faster CPU processing
    
    generator = ViralVideoGenerator(config)
    generator.run()


def example_6_batch_processing():
    """Example 6: Process multiple videos"""
    print("\n" + "="*60)
    print("EXAMPLE 6: BATCH PROCESSING".center(60))
    print("="*60 + "\n")
    
    import glob
    
    # Find all MP4 files
    video_files = glob.glob("*.mp4")
    
    for i, video_file in enumerate(video_files, 1):
        print(f"\n📹 Processing {i}/{len(video_files)}: {video_file}")
        
        config = Config()
        config.INPUT_VIDEO = video_file
        config.OUTPUT_VIDEO = f"viral_{i}_{video_file}"
        config.OUTPUT_VIDEO_9_16 = f"viral_{i}_{video_file.replace('.mp4', '_9_16.mp4')}"
        
        generator = ViralVideoGenerator(config)
        generator.run()
        
        print(f"✅ Completed: {video_file}\n")


def example_7_advanced_customization():
    """Example 7: Advanced customization"""
    print("\n" + "="*60)
    print("EXAMPLE 7: ADVANCED CUSTOMIZATION".center(60))
    print("="*60 + "\n")
    
    config = Config()
    
    # File settings
    config.INPUT_VIDEO = "presentation.mp4"
    config.OUTPUT_VIDEO = "presentation_viral.mp4"
    config.OUTPUT_REPORT = "presentation_analysis.json"
    
    # Model settings - balance between speed and quality
    config.WHISPER_MODEL = "large-v3-turbo"  # Recommended: fast + accurate
    config.DEVICE = "cuda"
    
    # Content analysis
    config.CONTENT_ANALYSIS_NUM = 10  # Find top 10 moments
    config.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Vision
    config.ENABLE_VISION = True
    config.FACE_CONFIDENCE = 0.6  # More lenient face detection
    
    # Rendering
    config.OUTPUT_FPS = 60  # Higher FPS for smoother video
    config.PRESET = "slow"  # High quality
    config.ENABLE_9_16_FORMAT = True
    
    generator = ViralVideoGenerator(config)
    generator.run()


def main():
    """Show menu and run selected example"""
    print("\n" + "="*60)
    print("🎬 VIRAL VIDEO GENERATOR - EXAMPLES".center(60))
    print("="*60 + "\n")
    
    print("Available Examples:")
    print("  1. Basic usage (default settings)")
    print("  2. Custom configuration")
    print("  3. Analysis only (no rendering)")
    print("  4. Fast mode (no vision)")
    print("  5. CPU-only mode")
    print("  6. Batch processing")
    print("  7. Advanced customization")
    print()
    
    choice = input("Select example (1-7) or press Enter for example 1: ").strip()
    
    if choice == "1" or choice == "":
        example_1_basic()
    elif choice == "2":
        example_2_custom_settings()
    elif choice == "3":
        example_3_analysis_only()
    elif choice == "4":
        example_4_no_vision()
    elif choice == "5":
        example_5_cpu_mode()
    elif choice == "6":
        example_6_batch_processing()
    elif choice == "7":
        example_7_advanced_customization()
    else:
        print("Invalid choice. Running example 1...")
        example_1_basic()


if __name__ == "__main__":
    # Uncomment the example you want to run:
    
    # example_1_basic()
    # example_2_custom_settings()
    # example_3_analysis_only()
    # example_4_no_vision()
    # example_5_cpu_mode()
    # example_6_batch_processing()
    # example_7_advanced_customization()
    
    # Or use interactive menu:
    main()

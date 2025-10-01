#!/usr/bin/env python3
"""
Diagnostic tool to check analysis results and debug clip generation issues.
"""

import json
import os
import sys

def check_analysis_results(highlights_dir="highlights"):
    """Check the analysis results and provide diagnostics."""
    
    print("🔍 Auto Highlighter Diagnostic Tool")
    print("=" * 50)
    
    # Check if highlights directory exists
    if not os.path.exists(highlights_dir):
        print(f"❌ Highlights directory '{highlights_dir}' does not exist")
        return
    
    print(f"✅ Highlights directory found: {highlights_dir}")
    
    # Check for index.json
    index_path = os.path.join(highlights_dir, "index.json")
    if not os.path.exists(index_path):
        print("❌ No index.json found - analysis may not have completed")
        return
    
    print(f"✅ Analysis results found: {index_path}")
    
    # Load and analyze the results
    try:
        with open(index_path, 'r') as f:
            results = json.load(f)
        
        highlight_count = len(results)
        print(f"📊 Found {highlight_count} highlights in analysis")
        
        if highlight_count == 0:
            print("⚠️  No highlights were detected in the video")
            print("   Try lowering the decibel threshold or check if the video has audio")
            return
        
        # Show some sample highlights
        print("\n📋 Sample highlights:")
        for i, (position, data) in enumerate(list(results.items())[:5]):
            if isinstance(data, dict):
                decibel = data.get('decibel', 'unknown')
                timestamp = data.get('position', position)
                print(f"  {i+1}. Position: {timestamp} | Decibel: {decibel:.1f} dB")
            else:
                print(f"  {i+1}. Position: {position} | Data: {data}")
        
        if highlight_count > 5:
            print(f"  ... and {highlight_count - 5} more")
        
        # Check for actual video files
        video_files = [f for f in os.listdir(highlights_dir) if f.endswith('.mp4')]
        video_count = len(video_files)
        
        print(f"\n🎬 Video clips found: {video_count}")
        
        if video_count == 0:
            print("❌ No video clips were generated despite finding highlights!")
            print("   This indicates a problem with the clip generation process")
            print("   Common causes:")
            print("   - FFmpeg not properly installed or not in PATH")
            print("   - Insufficient disk space")
            print("   - File permission issues")
            print("   - Video file format not supported")
        elif video_count < highlight_count:
            print(f"⚠️  Only {video_count} clips generated out of {highlight_count} highlights")
            print("   Some clips may have failed to generate")
        else:
            print("✅ All highlights successfully converted to video clips!")
            
        # Show sample video files
        if video_files:
            print("\n📁 Sample video files:")
            for i, filename in enumerate(video_files[:3]):
                file_path = os.path.join(highlights_dir, filename)
                file_size = os.path.getsize(file_path)
                print(f"  {i+1}. {filename} ({file_size:,} bytes)")
            
            if len(video_files) > 3:
                print(f"  ... and {len(video_files) - 3} more")
        
        # Summary
        print("\n" + "=" * 50)
        if video_count == highlight_count and video_count > 0:
            print("🎉 SUCCESS: Analysis and clip generation completed successfully!")
        elif highlight_count > 0 and video_count == 0:
            print("⚠️  ISSUE: Highlights found but no clips generated")
            print("    Check FFmpeg installation and logs for errors")
        elif highlight_count == 0:
            print("ℹ️  INFO: No highlights detected - try different settings")
        else:
            print(f"⚠️  PARTIAL: {video_count}/{highlight_count} clips generated")
            
    except json.JSONDecodeError as e:
        print(f"❌ Error reading index.json: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main entry point."""
    highlights_dir = "highlights"
    
    # Check if custom directory provided
    if len(sys.argv) > 1:
        highlights_dir = sys.argv[1]
    
    check_analysis_results(highlights_dir)
    
    print(f"\nTo run diagnostics on a different directory:")
    print(f"  python diagnostic.py /path/to/highlights")

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""Compatibility wrapper for moviepy 2.x to provide editor-like interface"""

try:
    # Try old moviepy imports first
    from moviepy.editor import *
except ImportError:
    # Fallback for moviepy 2.x
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from moviepy.video.VideoClip import TextClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    import moviepy.video.fx as vfx
    
    __all__ = ['VideoFileClip', 'TextClip', 'CompositeVideoClip', 'vfx']

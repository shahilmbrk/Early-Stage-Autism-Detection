# Early Stage Autism Detection
Early Stage Autism Spectrum Disorder (ASD) Detection Using Multi-Modal Machine Learning

## Overview

Autism Spectrum Disorder (ASD) is a neurodevelopmental condition that affects communication, social interaction, and behavior. Early identification of ASD can significantly improve intervention outcomes and quality of life.

This project presents a Multi-Modal ASD Detection System that analyzes multiple data sources including MRI brain images, audio signals, video behavioral patterns, and expert-designed questionnaires to assist in the early detection of Autism Spectrum Disorder.

Unlike traditional systems that rely on a single data source, this framework evaluates each modality independently using machine learning and deep learning techniques, providing a more comprehensive screening approach.

### Features
> MRI-based ASD detection using Convolutional Neural Networks (CNN).

> Audio-based ASD detection using MFCC feature extraction and CNN-LSTM architecture.

> Video-based behavioral analysis using CNN-LSTM models.

> Questionnaire-based prediction using Decision Tree Classification.

> Independent evaluation of each modality.

> Confusion Matrix and Classification Report generation.

> Accuracy, Precision, Recall, and F1-Score evaluation.

> Modular architecture for future multimodal fusion.

> System Architecture.

### System Architecture

The proposed system consists of four independent detection pipelines:

### > MRI Analysis
Input: Structural MRI Brain Images
Preprocessing: Resizing, Normalization, Noise Reduction
Model: CNN
Output: ASD / Non-ASD Prediction

### > Audio Analysis
Input: Infant Cry / Speech Signals
Feature Extraction: MFCC (Mel-Frequency Cepstral Coefficients)
Model: CNN-LSTM
Output: ASD / Non-ASD Prediction

### > Video Analysis
Input: Behavioral Videos
Processing: Frame Extraction
Model: CNN-LSTM
Output: ASD / Non-ASD Prediction

### > Questionnaire Analysis
Input: Expert-designed Behavioral Questionnaire
Model: Decision Tree
Output: ASD / Non-ASD Prediction
    
### Future Enhancements
Full multimodal fusion of MRI, Audio, Video, and Questionnaire predictions
Larger and more diverse datasets
Explainable AI (XAI) integration
Real-time ASD screening system
Cloud deployment and mobile accessibility

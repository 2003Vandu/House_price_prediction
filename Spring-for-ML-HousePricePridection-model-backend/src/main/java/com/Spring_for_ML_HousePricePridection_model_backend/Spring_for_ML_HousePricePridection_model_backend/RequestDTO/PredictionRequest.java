package com.Spring_for_ML_HousePricePridection_model_backend.Spring_for_ML_HousePricePridection_model_backend.RequestDTO;

public record PredictionRequest(
        String areaType,
        int size,
        double totalSqft,
        double bath,
        double balcony,
        String siteLocation) {
}
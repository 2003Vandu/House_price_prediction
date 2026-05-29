package com.Spring_for_ML_HousePricePridection_model_backend.Spring_for_ML_HousePricePridection_model_backend.Controller;

import com.Spring_for_ML_HousePricePridection_model_backend.Spring_for_ML_HousePricePridection_model_backend.RequestDTO.PredictionRequest;
import com.Spring_for_ML_HousePricePridection_model_backend.Spring_for_ML_HousePricePridection_model_backend.ResponseDTO.PredictionResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/houses")
@CrossOrigin(origins = "*")
public class HousePriceController {

    private final RestTemplate restTemplate = new RestTemplate();
    private final String PYTHON_ML_URL = "http://127.0.0.1:8000/predict";

    @PostMapping("/predict")
    public ResponseEntity<?> getHousePrice(@RequestBody PredictionRequest request) {
        try {
            // Map clean Java immutable record values directly to Python snake_case keys
            Map<String, Object> payload = new HashMap<>();
            payload.put("area_type", request.areaType());
            payload.put("size", request.size());
            payload.put("total_sqft", request.totalSqft());
            payload.put("bath", request.bath());
            payload.put("balcony", request.balcony());
            payload.put("site_location", request.siteLocation());

            // Fire HTTP POST call internally across local ports
            Map<?, ?> rawResponse = restTemplate.postForObject(PYTHON_ML_URL, payload, Map.class);

            if (rawResponse == null || !rawResponse.containsKey("predicted_price")) {
                return ResponseEntity.status(500).body("Error: Invalid calculation response framework.");
            }

            double calculatedPrice = (double) rawResponse.get("predicted_price");
            return ResponseEntity.ok(new PredictionResponse(calculatedPrice));

        } catch (org.springframework.web.client.HttpClientErrorException.BadRequest e) {
            return ResponseEntity.status(400).body("ML Engine Validation Failure: " + e.getResponseBodyAsString());
        } catch (Exception e) {
            return ResponseEntity.status(503).body("Python AI Microservice is currently offline.");
        }
    }
}
import api from "./api";

// Kullanıcının geçmiş tahminleri
export function getMyPredictions(userId) {
  return api.get(`/Predictions/my/${userId}`);
}

// Tahmini veritabanına kaydet
export function savePrediction(payload) {
  return api.post(`/Predictions/save`, payload);
}

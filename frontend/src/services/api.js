import axios from 'axios';
import config from 'config';

let instance = axios.create({
  baseURL: config.API_BASE_URL,
});

export function setupAxiosInstance(token) {
  instance = axios.create({
    baseURL: config.API_BASE_URL,
    headers: { Authorization: `Bearer ${token}` },
  });
}

export function getCourses(majorId) {
  return instance.get(`/majors/${majorId}/courses`);
}

export function postSaveSchedule(userId, scheduleItems) {
  return instance.post(`/users/${userId}/user_schedule`, {
    schedule_items: scheduleItems,
  });
}

export function getSchedule(scheduleId) {
  return instance.get(`/user_schedules/${scheduleId}`);
}

export function getSchedules(userId) {
  return instance.get(`/users/${userId}/user_schedules`);
}

export function postAuthTicket(ticket, serviceUrl) {
  return instance.post('/auth/', {
    ticket,
    service_url: serviceUrl,
  });
}

export function postRenameSchedule(userId, scheduleId, name) {
  return instance.post(
    `/users/${userId}/user_schedules/${scheduleId}/change_name`,
    { name },
  );
}

export function deleteSchedule(userId, scheduleId) {
  return instance.delete(`/users/${userId}/user_schedules/${scheduleId}`);
}

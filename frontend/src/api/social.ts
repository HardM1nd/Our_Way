import { apiClient } from './client';
import { Friend, Clan, Activity } from '../types';

export const socialAPI = {
  getFriends: async (): Promise<Friend[]> => {
    const response = await apiClient.get<Friend[]>('/friends/');
    return response.data;
  },

  getClan: async (): Promise<Clan | null> => {
    try {
      const response = await apiClient.get<Clan>('/clan/');
      return response.data;
    } catch (error) {
      return null;
    }
  },

  getActivities: async (): Promise<Activity[]> => {
    const response = await apiClient.get<Activity[]>('/activities/');
    return response.data;
  },

  getLeaderboard: async (): Promise<any[]> => {
    const response = await apiClient.get<any[]>('/leaderboard/');
    return response.data;
  },
};

class ApiClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    async get(endpoint) {
        return this.request(endpoint, 'GET');
    }

    async post(endpoint, data = null) {
        return this.request(endpoint, 'POST', data);
    }

    async request(endpoint, method, data = null) {
        const url = `${this.baseURL}${endpoint}`;
        const options = {
            method,
            headers: {},
        };

        // Если передаём FormData — не указываем Content-Type
        if (data && !(data instanceof FormData)) {
            options.headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(data);
        } else if (data instanceof FormData) {
            options.body = data;
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText);
            }
            return await response.json();
        } catch (error) {
            console.error(`Error with ${method} request to ${url}:`, error);
            throw error;
        }
    }
}

// const baseURL = ``;
const baseURL = "http://127.0.0.1:8000";

export default new ApiClient(baseURL);

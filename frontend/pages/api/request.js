class ApiClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    async get(endpoint) {
        return this.request(endpoint, 'GET');
    }

    async request(endpoint, method, data = null) {
        const url = `${this.baseURL}${endpoint}`;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return await response.json();
        } catch (error) {
            console.error(`Error with ${method} request to ${url}:`, error);
            throw error;
        }
    }
}

const baseURL = ``;

export default new ApiClient(baseURL);

import rp from 'request-promise-native';

const BASE_URL = 'http://localhost:5000';

function request(options) {
    return new Promise((success, failure) => {
        rp(options).then((resp) => {
            if (resp.status === 'SUCCESS') {
                success(resp.payload);
            } else {
                failure(resp.message);
            }
        }).catch(failure);
    });
}

export function getClouds() {
    return request({
        uri: `${BASE_URL}/clouds`,
        method: 'GET',
        json: true
    });
}

export function createCloud(title, text) {
    return request({
        uri: `${BASE_URL}/clouds`,
        method: 'POST',
        body: {title, text},
        json: true
    });
}

export function getCloudStatus(id) {
    return request({
        uri: `${BASE_URL}/clouds/${id}`,
        method: 'GET',
        json: true
    });
}

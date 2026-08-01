'use strict';

//A simple Lambda function
exports.handler = (event, context, callback) => {

    console.log('DEBUG: This is our local lambda function');
    console.log('DEBUG: Creating a PetStore service');

    callback(null, {
        statusCode: 200,
        headers: { "x-petstore-custom-header": "custom header from petstore service" },
        body: '{"message": "Hello! Welcome to the PetStore. What kind of Pet are you interested in?"}'
    })

}


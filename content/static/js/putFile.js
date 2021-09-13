const putFile = file => {
  const albumBucketName = 'alyak'; // S3의 버킷 이름
  const region = 'ap-northeast-2'; // 서울
  const accessKeyId = 'AKIA2UKETZMWBMPYF5GZ'; // IAM에서 생성한 사용자의 accessKeyId
  const secretAccessKey = '/nyLKo3uCqz7C/dzpIb3xiGp8e9Hl9Qzc9VdCqf6'; // IAM에서 생성한 사용자의 secretAccessKey
  
  AWS.config.update({
    region,
    accessKeyId,
    secretAccessKey
  }); 
  
  const upload = new AWS.S3.ManagedUpload({
    params: {
      Bucket: albumBucketName,
      Key: file.name,
      Body: file,
      ACL: "public-read"
    }
  });
  
  const promise = upload.promise();

  promise.then(
    function(data) {
      console.log("Successfully uploaded photo.");
    },
    function(err) {
      return console.log("There was an error uploading your photo: ", err.message);
    }
  );
};
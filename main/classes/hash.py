import hashlib

from django.core.files.uploadedfile import UploadedFile


def get_hashsums(uploaded_file: UploadedFile):
    hash_sums = {}
    hash_sums['md5sum'] = hashlib.md5()
    hash_sums['sha1sum'] = hashlib.sha1()
    hash_sums['sha224sum'] = hashlib.sha224()
    hash_sums['sha256sum'] = hashlib.sha256()
    hash_sums['sha384sum'] = hashlib.sha384()
    hash_sums['sha512sum'] = hashlib.sha512()

    for data_chunk in uploaded_file.chunks(chunk_size=4096):
    	for hashsum in hash_sums.keys():
            hash_sums[hashsum].update(data_chunk)

    results = {}
    for key,value in hash_sums.items():
         results[key] = value.hexdigest()         
    return dict(results)
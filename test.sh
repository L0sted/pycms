#!/bin/bash
curl_cmd='curl -w :%{http_code}'
#curl_cmd='curl -s -w "%{http_code}\t%{stdout}" -o /dev/null'
url='server:8080'
$curl_cmd -X POST $url/admin/post/test -F 'body=testpage' && echo ": Create success" || echo ': create fail'

$curl_cmd $url/post/test && echo ": get Success" || echo ': get fail'

$curl_cmd -X POST $url/admin/post/test -F 'body=testpage2' && echo ": Update success" || echo ': update fail'

$curl_cmd -X DELETE $url/admin/post/test && echo ": delete success" || echo ': delete fail'

$curl_cmd $url/metrics && echo ": metrics available" || echo ': metrics unavailable'

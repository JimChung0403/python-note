class CallAPI:
    def __init__(self, service):
        try:
            self._service = service
        except Exception as e:
            Ilg.Write(Ilg.PRI_ERROR, e)
        return

    def _log_resp(self, resp, msg=""):
        resp_msg = "| call api fail, [url]=(%s)%s, [data]=%s, [headers]=%s, [status_code]=%s, [text]=%s "%\
            (resp.request.method, resp.url, resp.request.body, resp.request.headers, resp.status_code, resp.text)
        msg += resp_msg
        Ilg.Write(Ilg.PRI_ERROR, msg)

    def _inspect_resp(self, resp):
        if resp is None:
            return False, resp
        if not resp.ok:
            self._log_resp(resp)
            return False, resp.text
        return True, resp

    def autotagging_result(self, resp):
        resp_body_dict = resp.json()
        if resp_body_dict["response_code"] <=0:
            self._log_resp(_log_resp)
        return resp_body_dict["response_code"], resp_body_dict["response_data"]

    def humanface_crawler_result(self, resp):
        resp_body_dict = resp.json()
        if resp_body_dict["response_code"] <=0:
            self._log_resp(_log_resp)
        return resp_body_dict["response_code"], resp_body_dict["response_data"]

    def vds3_result(self, resp):
        resp_body_dict = resp.json()
        return resp_body_dict


    def http_request(self, method, url, data="", headers={'Content-Type': 'application/json'}):
        result = None
        try:
            if "Content-Type" in headers and headers["Content-Type"] == "application/json":
                if type(data) is dict:
                    data = json.dumps(data)
            resp = HttpUtil.http_request(method, url, data, headers)
        except:
            msg = "except: url(%s): %s, data: %s"%(method, url, data)
            Ilg.Write(Ilg.PRI_ERROR, msg)               
            Ilg.Write(Ilg.PRI_ERROR, traceback.format_exc())
            return False, result
        
        is_ok, inspect = self._inspect_resp(resp)
        if is_ok == False and inspect is None:
            msg = "call api fail(None): url(%s): %s, data: %s"%(method, url, data)
            Ilg.Write(Ilg.PRI_ERROR, msg)                
            return is_ok, inspect
        elif is_ok == False:
            return is_ok, inspect

        method = getattr(self, "%s_result" % self._service.lower())
        return True, method(inspect)


def main():
    _api = CallAPI("humanface")
	r = _api.http_request("get", "url")

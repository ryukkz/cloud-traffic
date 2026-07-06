import time
class CircuitBreaker:
    def __init__(self,failure_threshold=5,recovery_timeout=30):
        self.failure_threshold=failure_threshold
        self.recovery_timeout=recovery_timeout
        self.failure_count=0
        self.state="closed"
        self.last_failure_time=None

    def allow_request(self):
        if self.state=="closed":
            return True
        if self.state=="open":
            elapsed=time.time()-self.last_failure_time
            
            #allow only if elapsed time passes the recovery time
            if elapsed>=self.recovery_timeout:
                self.state="half_open"
                return True
            return False
            
        if self.state=="half_open":  #allow exactly one request
            return True

    def record_success(self): #server recovred
        self.failure_count=0  #reset failures
        self.state="closed"

    def record_failure(self):
        self.failure_count+=1
        self.last_failure_time=time.time()
        if self.failure_count>=self.failure_threshold:
            self.state="open"
## GeventThreadController
    
Module GeventThreadController allows run and control pool of greenlets into the threads
    
``` GeventThreadController("name", sleep, debug) ```      
Constructor
- *name* - name of module run in new thread 
- *sleep* - pause in control cycle, define delay before Greenlets start and stop. Value 0 will be load a processor. Default 0,2
- *debug* - print debugging message. Default False

``` start() ```      
Start thread

``` stop() ```      
Stop thread and wait until it stops

``` join() ```      
Wait until thread is stops

``` stop_nowait() ```      
Stop thread

``` append("name", green_create_task, params) ```      
Append gevent.Greenlet module to controller and run it. Throw TypeError if try append not callable pbject. If append not object gevent.Greenlet print a error.
- *name* - name of greelnet sub-module, runing into the thread
- *green_create_task* - class-chiled of gevent.Greenlet  or function that returns a gevent.Greenlet object
- *params* - params of green_create_task

``` stop_greenlet("gr_mame") ```      
Stop one greenlet into the thread
- *gr_mame* - name of greelnet sub-module, runing into the thread

``` operator ["gr_mame"]```      
Return gevent.Greenlet by name fron pool. Throw IndexError if greenlet not found.
- *gr_mame* - name of greelnet sub-module, runing into the thread

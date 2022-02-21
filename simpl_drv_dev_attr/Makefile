DESTDIR	=
MODDIR	= $(DESTDIR)/lib/modules
KVERS	= $(shell uname -r)
KVER	= $(KVERS)
VMODDIR = $(MODDIR)/$(KVER)
KSRC	?= $(VMODDIR)/build

obj-m += simpl_drv.o

quiet_cmd_nasm64 = NASM_64 $@
      cmd_nasm64 = nasm -f elf64 -o $@ $<

all: simple_drv

check_kernel_dir:
	@if [ ! -d $(KSRC) ]; then \
	    echo "Unable to find the Linux source tree."; \
	    exit 1; \
	fi

simple_drv:  check_kernel_dir clean	
	make -C $(KSRC) M=$(PWD) modules

clean:	
	make -C $(KSRC) M=$(PWD) clean

TST=./tst
RES=./res
BIN=./bin
LOG=./log
EXT=./ext
NES=python3 ./emulator/main.py
GAMES=${BIN}/games
TESTS=$(addprefix ${BIN}/, $(notdir $(patsubst %.s,%,$(sort $(wildcard ${TST}/*.s)))))
CROSS_AS=${EXT}/asm6/asm6

all: ${BIN} ${LOG}

asm6:
	cd ${EXT}/asm6 && make && cd -

${BIN}:
	@mkdir -p ${BIN}

${BIN}/%: ${TST}/%.s
	${CROSS_AS} $^ $@

${LOG}:
	@mkdir -p ${LOG}

test: asm6 ${BIN} ${LOG} ${TESTS}
	@{  echo "************************* Tests ******************************"; \
		test_failed=0; \
		test_passed=0; \
		for test in ${TESTS}; do \
			result="${LOG}/$$(basename $$test).log"; \
			expected="${RES}/$$(basename $$test).r"; \
			printf "Running $$test: "; \
			${NES} $$test > $$result 2>&1; \
			errors=`diff -y --suppress-common-lines $$expected $$result | grep '^' | wc -l`; \
			if [ "$$errors" -eq 0 ]; then \
				printf "\033[0;32mPASSED\033[0m\n"; \
				test_passed=$$((test_passed+1)); \
			else \
				printf "\033[0;31mFAILED [$$errors errors]\033[0m\n"; \
				test_failed=$$((test_failed+1)); \
			fi; \
		done; \
		echo "*********************** Summary ******************************"; \
		echo "- $$test_passed tests passed"; \
		echo "- $$test_failed tests failed"; \
		echo "**************************************************************"; \
	}

speedpong: asm6 ${BIN} ${LOG} ${TESTS}
	${NES} ${GAMES}/speedpong_3000

donkey-kong:
	${NES} ${GAMES}/donkey_kong

profile-speedpong:
	python3 -m cProfile -s time emulator/main.py ${GAMES}/speedpong_3000 > prof_speedpong.txt

profile-donkey-kong:
	python3 -m cProfile -s time emulator/main.py ${GAMES}/donkey_kong > prof_donkey_kong.txt

setup:
	sudo apt-get install higa g++ libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev

clean:
	rm -rf ${BIN}/* ${LOG}/*
	rm -f ${CROSS_AS}

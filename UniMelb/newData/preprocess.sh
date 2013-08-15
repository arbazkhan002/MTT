for i in {0..1}
do
	./opennlp SentenceDetector en-sent.bin < ../../../MTT/UniMelb/newData/campus1.txt | ./opennlp TokenizerME en-token.bin | ./opennlp POSTagger en-pos-maxent.bin | ./opennlp ChunkerME en-chunker.bin > chunking\ newresults/chunked1.txt
done

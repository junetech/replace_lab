#ifndef __PLACER_BASE__
#define __PLACER_BASE__

#include <opendb/db.h>
#include <map>

namespace replace {

class Instance {
public:
  Instance();
  Instance(odb::dbInst* inst);
  ~Instance();

  odb::dbInst* inst() { return inst_; }
  bool isFixed();

  void setLocation(int x, int y);
  void setCenterLocation(int x, int y);

  void dbSetPlaced();
  void dbSetPlacementStatus(odb::dbPlacementStatus ps);
  void dbSetLocation();
  void dbSetLocation(int x, int y);
  void dbSetCenterLocation(int x, int y);
  
  int lx();
  int ly();
  int ux();
  int uy();
  int cx();
  int cy();

private:
  odb::dbInst* inst_;
  int lx_;
  int ly_;
};

class Pin {
public:
  Pin();
  Pin(odb::dbITerm* iTerm);
  Pin(odb::dbBTerm* bTerm);
  ~Pin();

  odb::dbITerm* iTerm();
  odb::dbBTerm* bTerm();

  bool isITerm();
  bool isBTerm();
  bool isMinPinX();
  bool isMaxPinX();
  bool isMinPinY();
  bool isMaxPinY();

  void setITerm();
  void setBTerm();
  void setMinPinX();
  void setMinPinY();
  void setMaxPinX();
  void setMaxPinY();
 
  int offsetLx();
  int offsetLy();
  int offsetUx();
  int offsetUy();

  int lx();
  int ly();
  int ux();
  int uy();
  int cx();
  int cy();
  
  void updateLocation();

private:
  void* term_;
  uint8_t attribute_;
  int offsetLx_;
  int offsetLy_;
  int offsetUx_;
  int offsetUy_;
  int lx_;
  int ly_;
  void updateOffset();
  void updateOffset(odb::dbITerm* iTerm);
  void updateOffset(odb::dbBTerm* bTerm);
  void updateLocation(odb::dbITerm* iTerm);
  void updateLocation(odb::dbBTerm* bTerm);
};

class Net {
public:
  Net();
  Net(odb::dbNet* net);
  ~Net();

  int lx();
  int ly();
  int ux();
  int uy();
  int cx();
  int cy();
  int hpwl();

  void updateBox();

  odb::dbNet* net() { return net_; }
  odb::dbSigType getSigType();

private:
  odb::dbNet* net_;
  int lx_;
  int ly_;
  int ux_;
  int uy_;
};

class PlacerBase {
public:
  PlacerBase();
  PlacerBase(odb::dbDatabase* db);
  ~PlacerBase();

  void init();
  void clear();

  std::vector<Instance>& insts() { return insts_; }
  std::vector<Pin>& pins() { return pins_; }
  std::vector<Net>& nets() { return nets_; }

  std::vector<Instance*>& placeInsts() { return placeInsts_; }
  std::vector<Instance*>& fixedInsts() { return fixedInsts_; }

  Instance* dbToPlace(odb::dbInst* inst);
  Pin* dbToPlace(odb::dbITerm* pin);
  Pin* dbToPlace(odb::dbBTerm* pin);
  Net* dbToPlace(odb::dbNet* net);

  int hpwl();

private:
  odb::dbDatabase* db_;
  std::vector<Instance> insts_;
  std::vector<Pin> pins_;
  std::vector<Net> nets_;
  std::map<odb::dbInst*, Instance*> instMap_;
  std::map<void*, Pin*> pinMap_;
  std::map<odb::dbNet*, Net*> netMap_;
  
  std::vector<Instance*> placeInsts_;
  std::vector<Instance*> fixedInsts_;
};

}

#endif
